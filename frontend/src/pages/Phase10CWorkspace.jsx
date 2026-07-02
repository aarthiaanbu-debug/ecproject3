import { useEffect, useMemo, useState } from "react";
import {
  BarChart3,
  CalendarDays,
  FileText,
  FolderKanban,
  MessagesSquare,
  RefreshCw,
  Sparkles,
  Users,
} from "lucide-react";
import {
  createMeeting,
  createMeetingAttendee,
  createMeetingNote,
  createProject,
  createProjectChannel,
  createProjectDocument10C,
  createProjectTask10C,
  createProjectTeam,
  createTeam,
  createTeamMember,
  generateAIMeetingSummary,
  getAIMeetingSummary10C,
  getMeetingNotes,
  getMeetings,
  getProjectCalendar,
  getProjectChannels10C,
  getProjectDocuments10C,
  getProjects,
  getProjectTasks10C,
  getProjectTeams,
  getProjectWorkload,
  getTeamMembers,
  getTeams,
  getTeamWorkload,
  getWorkspaces,
} from "../api/api";

const pageMeta = {
  teams: { title: "Teams", icon: Users },
  "team-details": { title: "Team Details", icon: Users },
  projects: { title: "Projects", icon: FolderKanban },
  "project-details": { title: "Project Details", icon: FolderKanban },
  "project-teams": { title: "Project Teams", icon: Users },
  "project-channels": { title: "Project Channels", icon: MessagesSquare },
  "project-tasks": { title: "Project Tasks", icon: FolderKanban },
  "project-documents": { title: "Project Documents", icon: FileText },
  "meeting-scheduler": { title: "Meeting Scheduler", icon: CalendarDays },
  "meeting-notes": { title: "Meeting Notes", icon: FileText },
  "ai-meeting-summary": { title: "AI Meeting Summary", icon: Sparkles },
  "project-calendar": { title: "Project Calendar", icon: CalendarDays },
  "team-workload": { title: "Team Workload Dashboard", icon: BarChart3 },
};

const viewConfig = {
  teams: {
    selectors: [],
    actions: [],
    panels: ["teams"],
  },
  "team-details": {
    selectors: ["team"],
    actions: [["team-member", "Add Team Member"]],
    panels: ["teams", "team-members"],
  },
  projects: {
    selectors: [],
    actions: [["project", "Create Project"]],
    panels: ["projects"],
  },
  "project-details": {
    selectors: ["project"],
    actions: [],
    panels: ["projects", "project-workload"],
  },
  "project-teams": {
    selectors: ["project", "team"],
    actions: [["project-team", "Attach Project Team"]],
    panels: ["project-teams"],
  },
  "project-channels": {
    selectors: ["project"],
    actions: [["channels", "Create Channels"]],
    panels: ["project-channels"],
  },
  "project-tasks": {
    selectors: ["project", "team"],
    actions: [["tasks", "Create Tasks"]],
    panels: ["project-tasks"],
  },
  "project-documents": {
    selectors: ["project"],
    actions: [["documents", "Create Documents"]],
    panels: ["project-documents"],
  },
  "meeting-scheduler": {
    selectors: ["project", "team"],
    actions: [["meeting", "Schedule Meeting"]],
    panels: ["meetings"],
  },
  "meeting-notes": {
    selectors: ["meeting"],
    actions: [["note", "Add Meeting Note"]],
    panels: ["meeting-notes"],
  },
  "ai-meeting-summary": {
    selectors: ["meeting"],
    actions: [["summary", "Generate AI Summary"]],
    panels: ["ai-summary"],
  },
  "project-calendar": {
    selectors: ["project"],
    actions: [],
    panels: ["project-calendar"],
  },
  "team-workload": {
    selectors: ["team"],
    actions: [],
    panels: ["team-workload"],
  },
};

const payloadItems = (data) => (Array.isArray(data) ? data : data?.items || []);
const storedNumber = (key, fallback) => Number(localStorage.getItem(key) || fallback);
const nowIso = () => new Date().toISOString().slice(0, 16);
const laterIso = () => new Date(Date.now() + 60 * 60 * 1000).toISOString().slice(0, 16);
const apiDate = (value) => (value ? new Date(value).toISOString() : null);

export default function Phase10CWorkspace({ view }) {
  const meta = pageMeta[view] || pageMeta.projects;
  const config = viewConfig[view] || viewConfig.projects;
  const Icon = meta.icon;
  const userId = storedNumber("user_id", 1);
  const [tenantId, setTenantId] = useState(storedNumber("tenant_id", 1));
  const [workspaceId, setWorkspaceId] = useState(storedNumber("workspace_id", 1));

  const [teams, setTeams] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [projects, setProjects] = useState([]);
  const [projectTeams, setProjectTeams] = useState([]);
  const [channels, setChannels] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [meetings, setMeetings] = useState([]);
  const [notes, setNotes] = useState([]);
  const [calendar, setCalendar] = useState([]);
  const [teamWorkload, setTeamWorkload] = useState(null);
  const [projectWorkload, setProjectWorkload] = useState(null);
  const [summary, setSummary] = useState(null);
  const [teamDraft, setTeamDraft] = useState({
    name: "",
    description: "",
  });
  const [selectedTeamId, setSelectedTeamId] = useState(storedNumber("team_id", 1));
  const [selectedProjectId, setSelectedProjectId] = useState(storedNumber("project_id", 1));
  const [selectedMeetingId, setSelectedMeetingId] = useState(storedNumber("meeting_id", 1));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const selectedTeam = useMemo(
    () => teams.find((team) => team.id === selectedTeamId),
    [selectedTeamId, teams]
  );
  const selectedProject = useMemo(
    () => projects.find((project) => project.id === selectedProjectId),
    [selectedProjectId, projects]
  );
  const selectedMeeting = useMemo(
    () => meetings.find((meeting) => meeting.id === selectedMeetingId),
    [selectedMeetingId, meetings]
  );

  const loadAll = async () => {
    setLoading(true);
    setError("");
    try {
      const workspaceRes = await getWorkspaces();
      const workspaceRows = payloadItems(workspaceRes.data);
      const storedWorkspace = workspaceRows.find(
        (workspace) => workspace.id === workspaceId
      );
      const fallbackWorkspace =
        workspaceRows.find((workspace) => workspace.tenant_id === tenantId) ||
        workspaceRows[0];
      const activeWorkspace = storedWorkspace || fallbackWorkspace;

      if (!activeWorkspace) {
        throw new Error("Create or select a workspace before continuing");
      }

      const activeTenantId = activeWorkspace.tenant_id;
      const activeWorkspaceId = activeWorkspace.id;
      setTenantId(activeTenantId);
      setWorkspaceId(activeWorkspaceId);
      localStorage.setItem("workspace_id", String(activeWorkspaceId));

      const [teamRes, projectRes, meetingRes] = await Promise.all([
        getTeams({
          tenant_id: activeTenantId,
          workspace_id: activeWorkspaceId,
        }),
        getProjects({
          tenant_id: activeTenantId,
          workspace_id: activeWorkspaceId,
        }),
        getMeetings({
          tenant_id: activeTenantId,
          workspace_id: activeWorkspaceId,
        }),
      ]);

      const nextTeams = payloadItems(teamRes.data);
      const nextProjects = payloadItems(projectRes.data);
      const nextMeetings = payloadItems(meetingRes.data);
      setTeams(nextTeams);
      setProjects(nextProjects);
      setMeetings(nextMeetings);

      const teamId = selectedTeamId || nextTeams[0]?.id;
      const projectId = selectedProjectId || nextProjects[0]?.id;
      const meetingId = selectedMeetingId || nextMeetings[0]?.id;

      if (teamId) {
        setSelectedTeamId(teamId);
        localStorage.setItem("team_id", String(teamId));
        const [membersRes, workloadRes] = await Promise.all([
          getTeamMembers(teamId),
          getTeamWorkload(teamId),
        ]);
        setTeamMembers(payloadItems(membersRes.data));
        setTeamWorkload(workloadRes.data);
      }

      if (projectId) {
        setSelectedProjectId(projectId);
        localStorage.setItem("project_id", String(projectId));
        const [projectTeamsRes, channelRes, taskRes, docRes, calRes, workloadRes] =
          await Promise.all([
            getProjectTeams(projectId),
            getProjectChannels10C(projectId),
            getProjectTasks10C(projectId),
            getProjectDocuments10C(projectId),
            getProjectCalendar(projectId),
            getProjectWorkload(projectId),
          ]);
        setProjectTeams(payloadItems(projectTeamsRes.data));
        setChannels(payloadItems(channelRes.data));
        setTasks(payloadItems(taskRes.data));
        setDocuments(payloadItems(docRes.data));
        setCalendar(calRes.data?.events || []);
        setProjectWorkload(workloadRes.data);
      }

      if (meetingId) {
        setSelectedMeetingId(meetingId);
        localStorage.setItem("meeting_id", String(meetingId));
        const [notesRes, summaryRes] = await Promise.allSettled([
          getMeetingNotes(meetingId),
          getAIMeetingSummary10C(meetingId),
        ]);
        setNotes(notesRes.status === "fulfilled" ? payloadItems(notesRes.value.data) : []);
        setSummary(summaryRes.status === "fulfilled" ? summaryRes.value.data : null);
      }
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          err.message ||
          "Workspace data could not be loaded"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const rememberTeam = (id) => {
    setSelectedTeamId(id);
    localStorage.setItem("team_id", String(id));
  };

  const rememberProject = (id) => {
    setSelectedProjectId(id);
    localStorage.setItem("project_id", String(id));
  };

  const rememberMeeting = (id) => {
    setSelectedMeetingId(id);
    localStorage.setItem("meeting_id", String(id));
  };

  const action = async (kind) => {
    setError("");
    try {
      if (kind === "team") {
        const res = await createTeam({
          tenant_id: tenantId,
          workspace_id: workspaceId,
          name: teamDraft.name.trim(),
          description: teamDraft.description.trim() || null,
          lead_user_id: userId,
          created_by: userId,
        });
        rememberTeam(res.data.id);
        setTeamDraft({ name: "", description: "" });
      }
      if (kind === "team-member" && selectedTeamId) {
        await createTeamMember({
          tenant_id: tenantId,
          workspace_id: workspaceId,
          team_id: selectedTeamId,
          user_id: userId,
          role: "Lead Engineer",
          allocation_percent: 100,
        });
      }
      if (kind === "project") {
        const res = await createProject({
          tenant_id: tenantId,
          workspace_id: workspaceId,
          name: "Enterprise Flow SaaS Development",
          slug: "enterprise-flow-saas-development",
          description: "Delivery project for collaboration, workflow, meetings, documents, and workload visibility.",
          status: "ACTIVE",
          owner_user_id: userId,
          created_by: userId,
        });
        rememberProject(res.data.id);
      }
      if (kind === "project-team" && selectedProjectId && selectedTeamId) {
        await createProjectTeam({
          tenant_id: tenantId,
          workspace_id: workspaceId,
          project_id: selectedProjectId,
          team_id: selectedTeamId,
          role: "Core Delivery",
        });
      }
      if (kind === "channels" && selectedProjectId) {
        await Promise.all(
          ["#backend", "#frontend", "#testing", "#deployment"].map((name) =>
            createProjectChannel({
              tenant_id: tenantId,
              workspace_id: workspaceId,
              project_id: selectedProjectId,
              name,
              description: `${name} project collaboration channel`,
              channel_type: "PUBLIC",
              created_by: userId,
            })
          )
        );
      }
      if (kind === "tasks" && selectedProjectId) {
        const titles = ["Implement Login API", "Create Dashboard UI", "Deploy Release Build"];
        await Promise.all(
          titles.map((title) =>
            createProjectTask10C({
              title,
              description: `${title} for Enterprise Flow SaaS Development`,
              organization_id: tenantId,
              project_id: selectedProjectId,
              team_id: selectedTeamId || null,
              assigned_to: String(userId),
              created_by: String(userId),
              priority: title.includes("Deploy") ? "high" : "medium",
              status: "todo",
            })
          )
        );
      }
      if (kind === "documents" && selectedProjectId) {
        await Promise.all(
          ["Requirement Specification.pdf", "API Contract.docx", "Deployment Guide.pdf"].map((fileName) =>
            createProjectDocument10C({
              tenant_id: tenantId,
              workspace_id: workspaceId,
              project_id: selectedProjectId,
              title: fileName.replace(/\.[^.]+$/, ""),
              file_name: fileName,
              file_path: `/uploads/${fileName}`,
              document_type: fileName.endsWith(".pdf") ? "PDF" : "DOCX",
              uploaded_by: userId,
            })
          )
        );
      }
      if (kind === "meeting" && selectedProjectId) {
        const res = await createMeeting({
          tenant_id: tenantId,
          workspace_id: workspaceId,
          project_id: selectedProjectId,
          team_id: selectedTeamId || null,
          title: "Sprint Planning",
          agenda: "Plan sprint scope, owners, risks, and release readiness.",
          meeting_type: "SPRINT",
          location: "Engineering Workspace",
          starts_at: apiDate(nowIso()),
          ends_at: apiDate(laterIso()),
          status: "SCHEDULED",
          created_by: userId,
        });
        rememberMeeting(res.data.id);
        await createMeetingAttendee({
          tenant_id: tenantId,
          meeting_id: res.data.id,
          user_id: userId,
          response_status: "ACCEPTED",
          is_required: true,
        });
      }
      if (kind === "note" && selectedMeetingId) {
        await createMeetingNote({
          tenant_id: tenantId,
          meeting_id: selectedMeetingId,
          author_id: userId,
          content: "Sprint Planning covered login API, dashboard UI, QA test scope, and deployment sequencing.",
          decisions: "Backend Team owns Login API. Frontend Team owns Dashboard UI. DevOps owns release build.",
          action_items: "QA Team prepares regression checklist. Client demo remains on the release calendar.",
        });
      }
      if (kind === "summary" && selectedMeetingId) {
        const res = await generateAIMeetingSummary(selectedMeetingId, userId);
        setSummary(res.data);
      }
      await loadAll();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Action failed");
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 p-4 text-zinc-100 sm:p-6">
      <div className="mx-auto max-w-7xl">
        <header className="mb-5 flex flex-col gap-4 border-b border-zinc-800 pb-5 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <div className="grid h-11 w-11 place-items-center rounded-md bg-emerald-500 text-zinc-950">
              <Icon size={22} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">{meta.title}</h1>
              <p className="text-sm text-zinc-400">
                Tenant {tenantId} / Engineering Workspace {workspaceId} / Enterprise Flow SaaS Development
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={loadAll}
            className="inline-flex items-center justify-center gap-2 rounded-md bg-zinc-800 px-4 py-2 text-sm font-semibold hover:bg-zinc-700"
          >
            <RefreshCw size={16} /> Refresh
          </button>
        </header>

        {error && <div className="mb-4 rounded-md border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-100">{error}</div>}

        {view === "teams" && (
          <form
            className="mb-5 grid gap-3 rounded-md border border-zinc-800 bg-zinc-900 p-4 md:grid-cols-[1fr_2fr_auto]"
            onSubmit={(event) => {
              event.preventDefault();
              if (teamDraft.name.trim()) {
                action("team");
              }
            }}
          >
            <label className="block">
              <span className="mb-2 block text-xs font-semibold uppercase text-zinc-500">Team name</span>
              <input
                required
                value={teamDraft.name}
                onChange={(event) =>
                  setTeamDraft((current) => ({ ...current, name: event.target.value }))
                }
                placeholder="Backend Team"
                className="w-full rounded-md border border-zinc-700 bg-zinc-950 p-2 text-sm"
              />
            </label>
            <label className="block">
              <span className="mb-2 block text-xs font-semibold uppercase text-zinc-500">Description</span>
              <input
                value={teamDraft.description}
                onChange={(event) =>
                  setTeamDraft((current) => ({ ...current, description: event.target.value }))
                }
                placeholder="Responsible for backend API development"
                className="w-full rounded-md border border-zinc-700 bg-zinc-950 p-2 text-sm"
              />
            </label>
            <button
              type="submit"
              className="self-end rounded-md bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500"
            >
              Create Team
            </button>
          </form>
        )}

        {config.selectors.length > 0 && (
          <section className="mb-5 grid gap-3 lg:grid-cols-3">
            {config.selectors.includes("team") && (
              <Selector title="Team" value={selectedTeamId} onChange={rememberTeam} rows={teams} />
            )}
            {config.selectors.includes("project") && (
              <Selector title="Project" value={selectedProjectId} onChange={rememberProject} rows={projects} />
            )}
            {config.selectors.includes("meeting") && (
              <Selector title="Meeting" value={selectedMeetingId} onChange={rememberMeeting} rows={meetings} />
            )}
          </section>
        )}

        {config.actions.length > 0 && (
          <section className="mb-5 flex flex-wrap gap-2">
            {config.actions.map(([kind, label]) => (
              <ActionButton key={kind} onClick={() => action(kind)} label={label} />
            ))}
          </section>
        )}

        {loading ? (
          <p className="text-zinc-400">Loading workspace...</p>
        ) : (
          <main className="grid gap-4 xl:grid-cols-2">
            {config.panels.includes("teams") && (
              <DataPanel title="Teams" rows={teams} fields={["id", "name", "description", "is_active"]} highlight={selectedTeam?.name} />
            )}
            {config.panels.includes("team-members") && (
              <DataPanel title="Team Members" rows={teamMembers} fields={["id", "team_id", "user_id", "role", "allocation_percent"]} />
            )}
            {config.panels.includes("projects") && (
              <DataPanel title="Projects" rows={projects} fields={["id", "name", "status", "slug"]} highlight={selectedProject?.name} />
            )}
            {config.panels.includes("project-teams") && (
              <DataPanel title="Project Teams" rows={projectTeams} fields={["id", "project_id", "team_id", "role", "is_active"]} />
            )}
            {config.panels.includes("project-channels") && (
              <DataPanel title="Project Channels" rows={channels} fields={["id", "name", "channel_type", "project_id"]} />
            )}
            {config.panels.includes("project-tasks") && (
              <DataPanel title="Project Tasks" rows={tasks} fields={["id", "title", "status", "priority", "team_id"]} />
            )}
            {config.panels.includes("project-documents") && (
              <DataPanel title="Project Documents" rows={documents} fields={["id", "title", "file_name", "document_type"]} />
            )}
            {config.panels.includes("meetings") && (
              <DataPanel title="Meetings" rows={meetings} fields={["id", "title", "status", "starts_at"]} highlight={selectedMeeting?.title} />
            )}
            {config.panels.includes("meeting-notes") && (
              <DataPanel title="Meeting Notes" rows={notes} fields={["id", "author_id", "content", "decisions"]} />
            )}
            {config.panels.includes("project-calendar") && (
              <DataPanel title="Project Calendar" rows={calendar} fields={["id", "type", "title", "status", "starts_at"]} />
            )}
            {config.panels.includes("team-workload") && <MetricPanel title="Team Workload" data={teamWorkload} />}
            {config.panels.includes("project-workload") && <MetricPanel title="Project Workload" data={projectWorkload} />}
            {config.panels.includes("ai-summary") && (
              <section className="xl:col-span-2 rounded-md border border-zinc-800 bg-zinc-900 p-4">
                <h2 className="mb-3 font-semibold">AI Meeting Summary</h2>
                <p className="text-sm leading-6 text-zinc-300">{summary?.summary || "Generate a summary after adding notes."}</p>
                {summary?.key_decisions && <p className="mt-3 text-sm text-zinc-400">Decisions: {summary.key_decisions}</p>}
                {summary?.action_items && <p className="mt-2 text-sm text-zinc-400">Actions: {summary.action_items}</p>}
              </section>
            )}
          </main>
        )}
      </div>
    </div>
  );
}

function Selector({ title, rows, value, onChange }) {
  return (
    <label className="block rounded-md border border-zinc-800 bg-zinc-900 p-3">
      <span className="mb-2 block text-xs font-semibold uppercase text-zinc-500">{title}</span>
      <select
        className="w-full rounded-md border border-zinc-700 bg-zinc-950 p-2 text-sm"
        value={value || ""}
        onChange={(event) => onChange(Number(event.target.value))}
      >
        <option value="">Select {title}</option>
        {rows.map((row) => (
          <option key={row.id} value={row.id}>
            #{row.id} {row.name || row.title}
          </option>
        ))}
      </select>
    </label>
  );
}

function ActionButton({ label, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-500"
    >
      {label}
    </button>
  );
}

function DataPanel({ title, rows, fields, highlight }) {
  return (
    <section className="rounded-md border border-zinc-800 bg-zinc-900 p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-semibold">{title}</h2>
        <span className="rounded bg-zinc-800 px-2 py-1 text-xs text-zinc-300">{rows.length}</span>
      </div>
      {highlight && <p className="mb-3 text-sm text-emerald-300">{highlight}</p>}
      <div className="space-y-2">
        {rows.map((row) => (
          <div key={row.id} className="rounded-md border border-zinc-800 bg-zinc-950 p-3 text-sm">
            {fields.map((field) => (
              <p key={field} className="break-words text-zinc-300">
                <span className="text-zinc-500">{field}:</span> {String(row[field] ?? "")}
              </p>
            ))}
          </div>
        ))}
        {rows.length === 0 && <p className="text-sm text-zinc-500">No records yet.</p>}
      </div>
    </section>
  );
}

function MetricPanel({ title, data }) {
  return (
    <section className="rounded-md border border-zinc-800 bg-zinc-900 p-4">
      <h2 className="mb-3 font-semibold">{title}</h2>
      <pre className="overflow-auto rounded-md bg-zinc-950 p-3 text-xs text-zinc-300">
        {JSON.stringify(data || {}, null, 2)}
      </pre>
    </section>
  );
}
