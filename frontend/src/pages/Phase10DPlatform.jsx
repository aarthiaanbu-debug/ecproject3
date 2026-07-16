import { useEffect, useMemo, useState } from "react";
import { BarChart3, BookOpen, FileText, Play, Plus, Save, Search, SlidersHorizontal, Trash2 } from "lucide-react";
import {
  addCustomFormField,
  addWorkflowRule,
  archiveKnowledgeArticle,
  createCustomForm,
  createKnowledgeArticle,
  createKnowledgeCategory,
  createNotificationRule,
  createWorkflow,
  deleteSavedSearch,
  disableCustomForm,
  disableNotificationRule,
  disableWorkflow,
  executeWorkflow,
  getCustomFormFields,
  getCustomForms,
  getKnowledgeArticles,
  getKnowledgeCategories,
  getNotificationRules,
  getPhase10DAnalytics,
  getReport,
  getSavedSearches,
  getWorkflowExecutions,
  getWorkflowRules,
  getWorkflows,
  globalSearch,
  saveSearch,
} from "../services/api";

const pageConfig = {
  workflows: { title: "Workflow Builder", icon: SlidersHorizontal },
  notificationRules: { title: "Notification Rules", icon: Save },
  globalSearch: { title: "Global Search", icon: Search },
  savedSearches: { title: "Saved Searches", icon: Save },
  analyticsDashboard: { title: "Analytics Dashboard", icon: BarChart3, area: "tasks" },
  projectAnalytics: { title: "Project Analytics", icon: BarChart3, area: "projects" },
  teamAnalytics: { title: "Team Analytics", icon: BarChart3, area: "teams" },
  taskAnalytics: { title: "Task Analytics", icon: BarChart3, area: "tasks" },
  approvalAnalytics: { title: "Approval Analytics", icon: BarChart3, area: "approvals" },
  documentAnalytics: { title: "Document Analytics", icon: BarChart3, area: "documents" },
  knowledgeBase: { title: "Knowledge Base", icon: BookOpen },
  articleEditor: { title: "Article Editor", icon: BookOpen },
  customForms: { title: "Custom Forms", icon: SlidersHorizontal },
  reports: { title: "Reports", icon: FileText },
};

const tenantId = () => Number(localStorage.getItem("tenant_id") || 1);
const userId = () => Number(localStorage.getItem("user_id") || 1);
const itemsOf = (payload) => payload?.items || payload || [];

function Field({ label, children }) {
  return (
    <label className="block">
      <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</span>
      <div className="mt-1">{children}</div>
    </label>
  );
}

function inputClass() {
  return "w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 outline-none focus:border-cyan-500";
}

function Panel({ title, children, action }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-base font-bold text-slate-900">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  );
}

function Empty({ text }) {
  return <p className="rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">{text}</p>;
}

function Workflows() {
  const [workflows, setWorkflows] = useState([]);
  const [selected, setSelected] = useState(null);
  const [rules, setRules] = useState([]);
  const [executions, setExecutions] = useState([]);
  const [form, setForm] = useState({ name: "", workflow_type: "TASK", description: "" });
  const [rule, setRule] = useState({ trigger_event: "TASK_OVERDUE", condition_type: "DAYS_OVERDUE", condition_value: "2", action_type: "NOTIFICATION", action_value: "Notify project owner" });

  const load = async () => {
    const res = await getWorkflows({ tenant_id: tenantId() });
    setWorkflows(itemsOf(res.data));
  };

  const loadDetails = async (workflow) => {
    setSelected(workflow);
    const [rulesRes, executionsRes] = await Promise.all([getWorkflowRules(workflow.id), getWorkflowExecutions(workflow.id)]);
    setRules(itemsOf(rulesRes.data));
    setExecutions(itemsOf(executionsRes.data));
  };

  useEffect(() => { load(); }, []);

  const create = async (event) => {
    event.preventDefault();
    await createWorkflow({ tenant_id: tenantId(), ...form });
    setForm({ name: "", workflow_type: "TASK", description: "" });
    await load();
  };

  const createRule = async (event) => {
    event.preventDefault();
    if (!selected) return;
    await addWorkflowRule(selected.id, rule);
    await loadDetails(selected);
  };

  return (
    <div className="grid gap-4 xl:grid-cols-[360px_1fr]">
      <Panel title="Create Workflow">
        <form onSubmit={create} className="space-y-3">
          <Field label="Name"><input className={inputClass()} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></Field>
          <Field label="Type">
            <select className={inputClass()} value={form.workflow_type} onChange={(e) => setForm({ ...form, workflow_type: e.target.value })}>
              {["TASK", "APPROVAL", "PROJECT", "MEETING"].map((item) => <option key={item}>{item}</option>)}
            </select>
          </Field>
          <Field label="Description"><textarea className={inputClass()} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></Field>
          <button className="inline-flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white"><Plus size={16} />Create</button>
        </form>
      </Panel>

      <Panel title="Workflows">
        <div className="grid gap-3 lg:grid-cols-2">
          {workflows.map((item) => (
            <button key={item.id} onClick={() => loadDetails(item)} className="rounded-lg border border-slate-200 p-3 text-left hover:border-cyan-400">
              <div className="flex items-center justify-between gap-2">
                <strong>{item.name}</strong>
                <span className="text-xs text-slate-500">{item.workflow_type}</span>
              </div>
              <p className="mt-1 text-sm text-slate-500">{item.description || "No description"}</p>
              <div className="mt-3 flex gap-2">
                <span className={`rounded px-2 py-1 text-xs ${item.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"}`}>{item.is_active ? "Active" : "Disabled"}</span>
                <button className="rounded border px-2 py-1 text-xs" onClick={(e) => { e.stopPropagation(); disableWorkflow(item.id).then(load); }}>Disable</button>
              </div>
            </button>
          ))}
        </div>
        {!workflows.length && <Empty text="No workflows have been created." />}
      </Panel>

      <Panel title={selected ? `Rules for ${selected.name}` : "Workflow Rules"}>
        {selected ? (
          <form onSubmit={createRule} className="grid gap-3 md:grid-cols-2">
            <Field label="Trigger"><input className={inputClass()} value={rule.trigger_event} onChange={(e) => setRule({ ...rule, trigger_event: e.target.value })} /></Field>
            <Field label="Condition"><input className={inputClass()} value={rule.condition_type} onChange={(e) => setRule({ ...rule, condition_type: e.target.value })} /></Field>
            <Field label="Value"><input className={inputClass()} value={rule.condition_value} onChange={(e) => setRule({ ...rule, condition_value: e.target.value })} /></Field>
            <Field label="Action">
              <select className={inputClass()} value={rule.action_type} onChange={(e) => setRule({ ...rule, action_type: e.target.value })}>
                {["NOTIFICATION", "ESCALATION", "STATUS_UPDATE"].map((item) => <option key={item}>{item}</option>)}
              </select>
            </Field>
            <Field label="Action Value"><input className={inputClass()} value={rule.action_value} onChange={(e) => setRule({ ...rule, action_value: e.target.value })} /></Field>
            <div className="flex items-end gap-2">
              <button className="inline-flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white"><Plus size={16} />Add Rule</button>
              <button type="button" className="inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-bold" onClick={() => executeWorkflow(selected.id, { entity_type: selected.workflow_type, entity_id: 1 }).then(() => loadDetails(selected))}><Play size={16} />Run</button>
            </div>
          </form>
        ) : <Empty text="Select a workflow to manage rules." />}
        <div className="mt-4 grid gap-3 md:grid-cols-2">
          {rules.map((item) => <div key={item.id} className="rounded-lg bg-slate-50 p-3 text-sm"><strong>{item.trigger_event}</strong><p>{item.condition_type}: {item.condition_value}</p><p>{item.action_type}: {item.action_value}</p></div>)}
        </div>
      </Panel>

      <Panel title="Execution History">
        {executions.length ? executions.map((item) => <div key={item.id} className="mb-2 rounded-lg bg-slate-50 p-3 text-sm">{item.execution_status} at {item.executed_at}<p className="text-slate-500">{item.details}</p></div>) : <Empty text="No workflow executions yet." />}
      </Panel>
    </div>
  );
}

function NotificationRules() {
  const [rules, setRules] = useState([]);
  const [form, setForm] = useState({ event_type: "Task Assigned", notification_type: "IN_APP", recipient_role: "manager", message_template: "A task needs attention" });
  const load = async () => setRules(itemsOf((await getNotificationRules({ tenant_id: tenantId() })).data));
  useEffect(() => { load(); }, []);
  const submit = async (event) => {
    event.preventDefault();
    await createNotificationRule({ tenant_id: tenantId(), ...form });
    await load();
  };
  return (
    <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
      <Panel title="Create Rule">
        <form onSubmit={submit} className="space-y-3">
          <Field label="Event"><input className={inputClass()} value={form.event_type} onChange={(e) => setForm({ ...form, event_type: e.target.value })} /></Field>
          <Field label="Type"><select className={inputClass()} value={form.notification_type} onChange={(e) => setForm({ ...form, notification_type: e.target.value })}><option>IN_APP</option><option>EMAIL</option></select></Field>
          <Field label="Recipient Role"><input className={inputClass()} value={form.recipient_role} onChange={(e) => setForm({ ...form, recipient_role: e.target.value })} /></Field>
          <Field label="Template"><textarea className={inputClass()} value={form.message_template} onChange={(e) => setForm({ ...form, message_template: e.target.value })} /></Field>
          <button className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white">Create Rule</button>
        </form>
      </Panel>
      <Panel title="Rules">
        <div className="grid gap-3 md:grid-cols-2">
          {rules.map((item) => (
            <div key={item.id} className="rounded-lg border border-slate-200 p-3">
              <div className="flex justify-between gap-2"><strong>{item.event_type}</strong><span className="text-xs">{item.notification_type}</span></div>
              <p className="mt-1 text-sm text-slate-500">{item.message_template || "No template"}</p>
              <button className="mt-3 inline-flex items-center gap-2 rounded border px-3 py-1 text-sm" onClick={() => disableNotificationRule(item.id).then(load)}><Trash2 size={14} />Disable</button>
            </div>
          ))}
        </div>
        {!rules.length && <Empty text="No notification rules yet." />}
      </Panel>
    </div>
  );
}

function SearchPage({ savedOnly = false }) {
  const [query, setQuery] = useState("Authentication API");
  const [results, setResults] = useState({});
  const [saved, setSaved] = useState([]);
  const loadSaved = async () => setSaved(itemsOf((await getSavedSearches({ tenant_id: tenantId(), user_id: userId() })).data));
  useEffect(() => { loadSaved(); }, []);
  const run = async () => {
    const res = await globalSearch({ tenant_id: tenantId(), q: query });
    setResults(res.data.results || {});
  };
  const save = async () => {
    await saveSearch({ tenant_id: tenantId(), user_id: userId(), name: query, query_json: { q: query, scope: "global" } });
    await loadSaved();
  };
  if (savedOnly) {
    return <Panel title="Saved Searches">{saved.map((item) => <div key={item.id} className="mb-2 flex items-center justify-between rounded-lg border p-3"><span>{item.name}</span><button onClick={() => deleteSavedSearch(item.id).then(loadSaved)}><Trash2 size={16} /></button></div>)}{!saved.length && <Empty text="No saved searches." />}</Panel>;
  }
  return (
    <div className="space-y-4">
      <Panel title="Enterprise Search">
        <div className="flex flex-col gap-3 md:flex-row">
          <input className={inputClass()} value={query} onChange={(e) => setQuery(e.target.value)} />
          <button className="inline-flex items-center justify-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 font-bold text-white" onClick={run}><Search size={16} />Search</button>
          <button className="inline-flex items-center justify-center gap-2 rounded-lg border px-4 py-2 font-bold" onClick={save}><Save size={16} />Save</button>
        </div>
      </Panel>
      <div className="grid gap-4 lg:grid-cols-2">
        {Object.entries(results).map(([type, rows]) => (
          <Panel key={type} title={type.replaceAll("_", " ")}>
            {rows.length ? rows.map((item) => <div key={`${item.type}-${item.id}`} className="mb-2 rounded-lg bg-slate-50 p-3 text-sm"><strong>{item.title}</strong><p className="text-slate-500">{item.type}</p></div>) : <Empty text="No matches." />}
          </Panel>
        ))}
      </div>
    </div>
  );
}

function Analytics({ area }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    getPhase10DAnalytics(area, { tenant_id: tenantId() }).then((res) => setData(res.data));
  }, [area]);
  const entries = useMemo(() => Object.entries(data?.data?.by_status || data?.data || {}), [data]);
  return (
    <Panel title="Metrics">
      {!data ? <Empty text="Loading analytics." /> : (
        <div className="grid gap-3 md:grid-cols-3">
          {entries.map(([key, value]) => (
            <div key={key} className="rounded-lg bg-slate-50 p-4">
              <p className="text-sm capitalize text-slate-500">{key.replaceAll("_", " ")}</p>
              <strong className="mt-2 block text-2xl text-slate-900">{Array.isArray(value) || typeof value === "object" ? JSON.stringify(value) : value}</strong>
            </div>
          ))}
        </div>
      )}
    </Panel>
  );
}

function Knowledge({ editor = false }) {
  const [categories, setCategories] = useState([]);
  const [articles, setArticles] = useState([]);
  const [category, setCategory] = useState({ name: "", description: "" });
  const [article, setArticle] = useState({ title: "", content: "", tags: "", category_id: "" });
  const load = async () => {
    const [catRes, articleRes] = await Promise.all([getKnowledgeCategories({ tenant_id: tenantId() }), getKnowledgeArticles({ tenant_id: tenantId() })]);
    setCategories(itemsOf(catRes.data));
    setArticles(itemsOf(articleRes.data));
  };
  useEffect(() => { load(); }, []);
  const createCategory = async (event) => {
    event.preventDefault();
    await createKnowledgeCategory({ tenant_id: tenantId(), ...category });
    setCategory({ name: "", description: "" });
    await load();
  };
  const createArticle = async (event) => {
    event.preventDefault();
    await createKnowledgeArticle({ tenant_id: tenantId(), created_by: userId(), ...article, category_id: article.category_id ? Number(article.category_id) : null });
    setArticle({ title: "", content: "", tags: "", category_id: "" });
    await load();
  };
  return (
    <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
      <Panel title={editor ? "Article Editor" : "Categories"}>
        {editor ? (
          <form onSubmit={createArticle} className="space-y-3">
            <Field label="Title"><input className={inputClass()} value={article.title} onChange={(e) => setArticle({ ...article, title: e.target.value })} /></Field>
            <Field label="Category"><select className={inputClass()} value={article.category_id} onChange={(e) => setArticle({ ...article, category_id: e.target.value })}><option value="">Uncategorized</option>{categories.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></Field>
            <Field label="Tags"><input className={inputClass()} value={article.tags} onChange={(e) => setArticle({ ...article, tags: e.target.value })} /></Field>
            <Field label="Content"><textarea rows={8} className={inputClass()} value={article.content} onChange={(e) => setArticle({ ...article, content: e.target.value })} /></Field>
            <button className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white">Publish Article</button>
          </form>
        ) : (
          <form onSubmit={createCategory} className="space-y-3">
            <Field label="Name"><input className={inputClass()} value={category.name} onChange={(e) => setCategory({ ...category, name: e.target.value })} /></Field>
            <Field label="Description"><textarea className={inputClass()} value={category.description} onChange={(e) => setCategory({ ...category, description: e.target.value })} /></Field>
            <button className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white">Create Category</button>
          </form>
        )}
      </Panel>
      <Panel title="Articles">
        <div className="grid gap-3 md:grid-cols-2">
          {articles.map((item) => (
            <article key={item.id} className="rounded-lg border border-slate-200 p-3">
              <strong>{item.title}</strong>
              <p className="mt-1 line-clamp-3 text-sm text-slate-500">{item.content}</p>
              <div className="mt-3 flex items-center justify-between text-xs text-slate-500"><span>v{item.version}</span><button onClick={() => archiveKnowledgeArticle(item.id).then(load)}>Archive</button></div>
            </article>
          ))}
        </div>
        {!articles.length && <Empty text="No knowledge articles yet." />}
      </Panel>
    </div>
  );
}

function Forms() {
  const [forms, setForms] = useState([]);
  const [selected, setSelected] = useState(null);
  const [fields, setFields] = useState([]);
  const [form, setForm] = useState({ name: "", description: "", request_type: "OTHER" });
  const [field, setField] = useState({ field_name: "", field_type: "TEXT", validation_rules: {}, is_required: false, sort_order: 0 });
  const load = async () => setForms(itemsOf((await getCustomForms({ tenant_id: tenantId() })).data));
  useEffect(() => { load(); }, []);
  const loadFields = async (item) => {
    setSelected(item);
    setFields(itemsOf((await getCustomFormFields(item.id)).data));
  };
  return (
    <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
      <Panel title="Create Form">
        <form onSubmit={async (e) => { e.preventDefault(); await createCustomForm({ tenant_id: tenantId(), ...form }); await load(); }} className="space-y-3">
          <Field label="Name"><input className={inputClass()} value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></Field>
          <Field label="Type"><select className={inputClass()} value={form.request_type} onChange={(e) => setForm({ ...form, request_type: e.target.value })}>{["LEAVE", "PURCHASE", "ACCESS", "LICENSE", "OTHER"].map((item) => <option key={item}>{item}</option>)}</select></Field>
          <Field label="Description"><textarea className={inputClass()} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} /></Field>
          <button className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white">Create Form</button>
        </form>
      </Panel>
      <Panel title="Forms">
        <div className="grid gap-3 md:grid-cols-2">
          {forms.map((item) => <button key={item.id} onClick={() => loadFields(item)} className="rounded-lg border p-3 text-left"><strong>{item.name}</strong><p className="text-sm text-slate-500">{item.request_type}</p><span className="mt-2 inline-block text-xs" onClick={(e) => { e.stopPropagation(); disableCustomForm(item.id).then(load); }}>Disable</span></button>)}
        </div>
      </Panel>
      <Panel title={selected ? `Fields for ${selected.name}` : "Fields"}>
        {selected ? (
          <form onSubmit={async (e) => { e.preventDefault(); await addCustomFormField(selected.id, field); await loadFields(selected); }} className="grid gap-3 md:grid-cols-2">
            <Field label="Field Name"><input className={inputClass()} value={field.field_name} onChange={(e) => setField({ ...field, field_name: e.target.value })} /></Field>
            <Field label="Field Type"><select className={inputClass()} value={field.field_type} onChange={(e) => setField({ ...field, field_type: e.target.value })}>{["TEXT", "NUMBER", "DATE", "SELECT", "FILE"].map((item) => <option key={item}>{item}</option>)}</select></Field>
            <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={field.is_required} onChange={(e) => setField({ ...field, is_required: e.target.checked })} /> Required</label>
            <button className="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-bold text-white">Add Field</button>
          </form>
        ) : <Empty text="Select a form to manage fields." />}
        <div className="mt-4 grid gap-2 md:grid-cols-3">{fields.map((item) => <div key={item.id} className="rounded-lg bg-slate-50 p-3 text-sm"><strong>{item.field_name}</strong><p>{item.field_type}</p></div>)}</div>
      </Panel>
    </div>
  );
}

function Reports() {
  const [type, setType] = useState("projects");
  const [report, setReport] = useState(null);
  const run = async () => setReport((await getReport(type, { tenant_id: tenantId() })).data);
  return (
    <div className="space-y-4">
      <Panel title="Report Filters">
        <div className="flex flex-col gap-3 md:flex-row">
          <select className={inputClass()} value={type} onChange={(e) => setType(e.target.value)}>{["projects", "tasks", "approvals", "documents"].map((item) => <option key={item}>{item}</option>)}</select>
          <button className="rounded-lg bg-cyan-600 px-4 py-2 font-bold text-white" onClick={run}>Generate</button>
          <button className="rounded-lg border px-4 py-2 font-bold" onClick={() => report && window.print()}>Export</button>
        </div>
      </Panel>
      <Panel title="Report Results">
        {report ? <pre className="max-h-[520px] overflow-auto rounded-lg bg-slate-950 p-4 text-xs text-slate-100">{JSON.stringify(report, null, 2)}</pre> : <Empty text="Generate a report to preview rows." />}
      </Panel>
    </div>
  );
}

export default function Phase10DPlatform({ view }) {
  const config = pageConfig[view] || pageConfig.workflows;
  const Icon = config.icon;
  let content = <Workflows />;
  if (view === "notificationRules") content = <NotificationRules />;
  if (view === "globalSearch") content = <SearchPage />;
  if (view === "savedSearches") content = <SearchPage savedOnly />;
  if (view?.includes("Analytics")) content = <Analytics area={config.area} />;
  if (view === "knowledgeBase") content = <Knowledge />;
  if (view === "articleEditor") content = <Knowledge editor />;
  if (view === "customForms") content = <Forms />;
  if (view === "reports") content = <Reports />;

  return (
    <main className="min-h-screen bg-slate-100 p-4 md:p-6">
      <div className="mb-5 flex items-center gap-3">
        <div className="rounded-lg bg-cyan-600 p-2 text-white"><Icon size={20} /></div>
        <div>
          <h1 className="text-2xl font-black text-slate-950">{config.title}</h1>
          <p className="text-sm text-slate-500">Platform services</p>
        </div>
      </div>
      {content}
    </main>
  );
}
