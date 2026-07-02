import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// TOKEN
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");

  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }

  return req;
});


// ================= AUTH =================

export const loginUser = (data) =>
  API.post("/auth/login", null, {
    params: data,
  });

export const registerUser = (data) =>
  API.post("/auth/register", null, {
    params: data,
  });


// ================= TASK =================

export const getTasks = () =>
  API.get("/task/all");

export const createTask = (data) =>
  API.post("/task/create", null, {
    params: data,
  });

export const updateTask = (id, status) =>
  API.put(`/task/update/${id}`, null, {
    params: { status },
  });

export const deleteTask = (id) =>
  API.delete(`/task/delete/${id}`);

export const assignTask = (id, user) =>
  API.put(`/task/assign/${id}`, null, {
    params: { user },
  });


// ================= KANBAN =================

export const getKanban = () =>
  API.get("/kanban");


// ================= APPROVAL =================

export const getApprovals = () =>
  API.get("/approval/all");

export const createApproval = (task_id) =>
  API.post("/approval/create", null, {
    params: { task_id },
  });


// ================= COMMENTS =================

export const getComments = (task_id) =>
  API.get(`/comments/${task_id}`);

export const addComment = (data) =>
  API.post(`/comments/${data.task_id}`, null, {
    params: { content: data.content },
  });

export const createComment = addComment;


// ================= ANALYTICS =================

export const getAnalytics = () =>
  API.get("/analytics/");


// ================= NOTIFICATIONS =================

export const getNotifications = () =>
  API.get("/notifications/");

export const markNotificationRead = (id) =>
  API.patch(`/notifications/${id}/read`);


// ================= AUDIT LOGS =================

export const getAuditLogs = () =>
  API.get("/audit-logs/");


// ================= DOCUMENTS =================

// UPLOAD
export const uploadDocument = (formData) =>
  API.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

// GET ALL DOCUMENTS
export const getDocuments = () =>
  API.get("/documents/");

// DELETE DOCUMENT
export const deleteDocument = (id) =>
  API.delete(`/documents/${id}`);

// AI SUMMARY
export const getAISummary = () =>
  API.get("/dashboard/ai-summary");

export const createStripeSession = (plan) =>
  API.post("/stripe/create-checkout-session", {
    plan: plan,
  });
  // ================= WORKSPACES =================

export const getWorkspaces = () =>
  API.get("/workspaces");

export const getWorkspace = (id) =>
  API.get(`/workspaces/${id}`);

export const createWorkspace = (data) =>
  API.post("/workspaces", data);

export const updateWorkspace = (id, data) =>
  API.put(`/workspaces/${id}`, data);

export const archiveWorkspace = (id) =>
  API.patch(`/workspaces/${id}/archive`);

export const restoreWorkspace = (id) =>
  API.patch(`/workspaces/${id}/restore`);


// ================= WORKSPACE MEMBERS =================

export const getWorkspaceMembers = (id) =>
  API.get(`/workspaces/${id}/members`);

export const addWorkspaceMember = (id, data) =>
  API.post(`/workspaces/${id}/members`, data);

export const updateWorkspaceMemberRole = (workspaceId, userId, role) =>
  API.patch(`/workspaces/${workspaceId}/members/${userId}/role`, { role });

export const removeWorkspaceMember = (workspaceId, userId) =>
  API.delete(`/workspaces/${workspaceId}/members/${userId}`);


// ================= CHANNELS =================

export const createChannel = (data) =>
  API.post("/channels", data);

export const getChannel = (id) =>
  API.get(`/channels/${id}`);

export const getWorkspaceChannels = (workspaceId) =>
  API.get(`/channels/workspace/${workspaceId}`);

export const updateChannel = (id, data) =>
  API.put(`/channels/${id}`, data);

export const archiveChannel = (id) =>
  API.patch(`/channels/${id}/archive`);

export const restoreChannel = (id) =>
  API.patch(`/channels/${id}/restore`);


// ================= CHANNEL MEMBERS =================

export const joinChannel = (channelId, userId) =>
  API.post(`/channels/${channelId}/join/${userId}`);

export const leaveChannel = (channelId, userId) =>
  API.post(`/channels/${channelId}/leave/${userId}`);


// ================= WORKSPACE MESSAGES =================

export const createWorkspaceMessage = (data) =>
  API.post("/workspace-messages", data);

export const getWorkspaceMessages = (workspaceId, params) =>
  API.get(`/workspace-messages/${workspaceId}`, { params });

export const updateWorkspaceMessage = (messageId, data) =>
  API.put(`/workspace-messages/${messageId}`, data);

export const deleteWorkspaceMessage = (messageId, params) =>
  API.delete(`/workspace-messages/${messageId}`, { params });


// ================= CHANNEL MESSAGES =================

export const createChannelMessage = (data) =>
  API.post("/channel-messages", data);

export const getChannelMessages = (channelId, params) =>
  API.get(`/channel-messages/${channelId}`, { params });

export const updateChannelMessage = (messageId, data) =>
  API.put(`/channel-messages/${messageId}`, data);

export const deleteChannelMessage = (messageId, params) =>
  API.delete(`/channel-messages/${messageId}`, { params });


// ================= WORKSPACE TASKS =================

export const createWorkspaceTask = (data) =>
  API.post("/workspace-tasks", data);

export const getWorkspaceTasks = (workspaceId) =>
  API.get(`/workspace-tasks/workspace/${workspaceId}`);

export const updateWorkspaceTask = (taskId, data) =>
  API.put(`/workspace-tasks/${taskId}`, data);

export const deleteWorkspaceTask = (taskId) =>
  API.delete(`/workspace-tasks/${taskId}`);


// ================= CHANNEL TASKS =================

export const createChannelTask = (data) =>
  API.post("/channel-tasks", data);

export const getChannelTasks = (channelId) =>
  API.get(`/channel-tasks/channel/${channelId}`);

export const updateChannelTask = (taskId, data) =>
  API.put(`/channel-tasks/${taskId}`, data);

export const deleteChannelTask = (taskId) =>
  API.delete(`/channel-tasks/${taskId}`);


// ================= TASK DOCUMENTS =================

export const uploadTaskDocument = (formData) =>
  API.post("/task-documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export const getTaskDocuments = (taskId, params) =>
  API.get(`/task-documents/task/${taskId}`, { params });

export const deleteTaskDocument = (documentId, params) =>
  API.delete(`/task-documents/${documentId}`, { params });

export const downloadTaskDocument = (documentId, params) =>
  API.get(`/task-documents/${documentId}/download`, {
    params,
    responseType: "blob",
  });


// ================= APPROVAL DOCUMENTS =================

export const uploadApprovalDocument = (formData) =>
  API.post("/approval-documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

export const getApprovalDocuments = (approvalId, params) =>
  API.get(`/approval-documents/approval/${approvalId}`, { params });

export const deleteApprovalDocument = (documentId, params) =>
  API.delete(`/approval-documents/${documentId}`, { params });

export const downloadApprovalDocument = (documentId, params) =>
  API.get(`/approval-documents/${documentId}/download`, {
    params,
    responseType: "blob",
  });

// ================= PHASE 10C ENTERPRISE PROJECT WORKFLOW =================

export const getTeams = (params) => API.get("/teams", { params });
export const getTeam = (id) => API.get(`/teams/${id}`);
export const createTeam = (data) => API.post("/teams", data);
export const updateTeam = (id, data) => API.put(`/teams/${id}`, data);
export const deleteTeam = (id) => API.delete(`/teams/${id}`);
export const getTeamMembers = (teamId, params) =>
  API.get(`/teams/${teamId}/members`, { params });
export const createTeamMember = (data) => API.post("/team-members", data);
export const updateTeamMember = (id, data) => API.put(`/team-members/${id}`, data);
export const deleteTeamMember = (id) => API.delete(`/team-members/${id}`);

export const getProjects = (params) => API.get("/projects", { params });
export const getProject = (id) => API.get(`/projects/${id}`);
export const createProject = (data) => API.post("/projects", data);
export const updateProject = (id, data) => API.put(`/projects/${id}`, data);
export const deleteProject = (id) => API.delete(`/projects/${id}`);
export const getProjectTeams = (projectId, params) =>
  API.get(`/projects/${projectId}/teams`, { params });
export const createProjectTeam = (data) => API.post("/project-teams", data);
export const updateProjectTeam = (id, data) => API.put(`/project-teams/${id}`, data);
export const deleteProjectTeam = (id) => API.delete(`/project-teams/${id}`);

export const getProjectChannels10C = (projectId, params) =>
  API.get(`/projects/${projectId}/channels`, { params });
export const createProjectChannel = (data) => API.post("/project-channels", data);
export const updateProjectChannel = (id, data) =>
  API.put(`/project-channels/${id}`, data);
export const deleteProjectChannel = (id) => API.delete(`/project-channels/${id}`);

export const getProjectTasks10C = (projectId, params) =>
  API.get(`/projects/${projectId}/tasks`, { params });
export const createProjectTask10C = (data) => API.post("/project-tasks", data);
export const updateProjectTask10C = (id, data) => API.put(`/project-tasks/${id}`, data);
export const deleteProjectTask10C = (id) => API.delete(`/project-tasks/${id}`);

export const getProjectDocuments10C = (projectId, params) =>
  API.get(`/projects/${projectId}/documents`, { params });
export const createProjectDocument10C = (data) => API.post("/project-documents", data);
export const updateProjectDocument10C = (id, data) =>
  API.put(`/project-documents/${id}`, data);
export const deleteProjectDocument10C = (id) =>
  API.delete(`/project-documents/${id}`);

export const getMeetings = (params) => API.get("/meetings", { params });
export const getMeeting = (id) => API.get(`/meetings/${id}`);
export const createMeeting = (data) => API.post("/meetings", data);
export const updateMeeting = (id, data) => API.put(`/meetings/${id}`, data);
export const deleteMeeting = (id) => API.delete(`/meetings/${id}`);
export const getMeetingAttendees = (meetingId, params) =>
  API.get(`/meetings/${meetingId}/attendees`, { params });
export const createMeetingAttendee = (data) => API.post("/meeting-attendees", data);
export const updateMeetingAttendee = (id, data) =>
  API.put(`/meeting-attendees/${id}`, data);
export const deleteMeetingAttendee = (id) => API.delete(`/meeting-attendees/${id}`);
export const getMeetingNotes = (meetingId, params) =>
  API.get(`/meetings/${meetingId}/notes`, { params });
export const createMeetingNote = (data) => API.post("/meeting-notes", data);
export const updateMeetingNote = (id, data) => API.put(`/meeting-notes/${id}`, data);
export const deleteMeetingNote = (id) => API.delete(`/meeting-notes/${id}`);
export const getAIMeetingSummary10C = (meetingId) =>
  API.get(`/ai-meeting-summary/${meetingId}`);
export const generateAIMeetingSummary = (meetingId, generatedBy) =>
  API.post(`/ai-meeting-summary/${meetingId}`, null, {
    params: { generated_by: generatedBy },
  });
export const getProjectCalendar = (projectId, params) =>
  API.get(`/project-calendar/${projectId}`, { params });
export const getTeamWorkload = (teamId) => API.get(`/workload/teams/${teamId}`);
export const getProjectWorkload = (projectId) =>
  API.get(`/workload/projects/${projectId}`);

export default API;
