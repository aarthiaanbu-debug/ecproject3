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
  API.post("/approval/create", { task_id });

export const updateApprovalStatus = (id, status) =>
  API.put(`/approval/${id}/status`, null, {
    params: { status },
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
// ================= STRIPE =================

export const createStripeSession = (data) =>
  API.post(
    "/stripe/create-checkout-session",
    typeof data === "string" ? { plan: data } : data
  );

export const getStripeSession = (sessionId) =>
  API.get(`/stripe/session/${sessionId}`);

// ================= PHASE 9 SLA =================

export const getSlaRules = () => API.get("/sla-rules");
export const createSlaRule = (data) => API.post("/sla-rules", data);
export const updateSlaRule = (id, data) => API.put(`/sla-rules/${id}`, data);
export const disableSlaRule = (id) => API.delete(`/sla-rules/${id}`);

export const getActiveSla = () => API.get("/sla-tracking/active");
export const getBreachedSla = () => API.get("/sla-tracking/breached");
export const getSlaByModule = (moduleName) =>
  API.get(`/sla-tracking/module/${moduleName}`);

export const getApprovalEscalations = () => API.get("/approval-escalations");
export const getPendingApprovalEscalations = () =>
  API.get("/approval-escalations/pending");
export const createApprovalEscalation = (data) =>
  API.post("/approval-escalations", data);
export const resolveApprovalEscalation = (id) =>
  API.put(`/approval-escalations/${id}/resolve`);
export const cancelApprovalEscalation = (id) =>
  API.put(`/approval-escalations/${id}/cancel`);

export const createApprovalDelegation = (data) =>
  API.post("/approval-delegations", data);
export const getMyApprovalDelegations = () => API.get("/approval-delegations/me");
export const getActiveApprovalDelegations = () =>
  API.get("/approval-delegations/active");
export const cancelApprovalDelegation = (id) =>
  API.put(`/approval-delegations/${id}/cancel`);

export const getNotificationPreferences = () =>
  API.get("/notification-preferences/me");
export const updateNotificationPreferences = (data) =>
  API.put("/notification-preferences/me", data);

export const getAuditLog = (id) => API.get(`/audit-logs/${id}`);
export const getAuditLogsByModule = (moduleName) =>
  API.get(`/audit-logs/module/${moduleName}`);
export const getAuditLogsByUser = (userId) => API.get(`/audit-logs/user/${userId}`);
export const getAuditLogsByDateRange = (params) =>
  API.get("/audit-logs/date-range", { params });

// ================= PHASE 10 TENANTS =================

export const getUsers = () => API.get("/users");
export const getTenants = () => API.get("/tenants");
export const createTenant = (data) => API.post("/tenants", data);
export const updateTenant = (id, data) => API.put(`/tenants/${id}`, data);
export const assignUserToTenant = (data) => API.post("/tenants/assign-user", data);
export const getTenantUsers = (tenantId) => API.get(`/tenants/${tenantId}/users`);
export const getTenantUsage = (tenantId) => API.get(`/tenants/${tenantId}/usage`);
export const getAllTenantUsage = () => API.get("/tenants/usage");

// ================= LEAVE REQUESTS =================

export const getLeaveRequests = () => API.get("/leave-requests");
export const createLeaveRequest = (data) => API.post("/leave-requests", data);
export const updateLeaveRequestStatus = (id, status) =>
  API.put(`/leave-requests/${id}/status`, null, {
    params: { status },
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

export const updateWorkspaceMemberRole = (
  workspaceId,
  userId,
  role
) =>
  API.patch(
    `/workspaces/${workspaceId}/members/${userId}/role`,
    { role }
  );

export const removeWorkspaceMember = (
  workspaceId,
  userId
) =>
  API.delete(
    `/workspaces/${workspaceId}/members/${userId}`
  );


// ================= CHANNELS =================

export const createChannel = (data) =>
  API.post("/channels", data);

export const getChannel = (id) =>
  API.get(`/channels/${id}`);

export const getWorkspaceChannels = (id) =>
  API.get(`/channels/workspace/${id}`);

export const updateChannel = (id, data) =>
  API.put(`/channels/${id}`, data);

export const archiveChannel = (id) =>
  API.patch(`/channels/${id}/archive`);

export const restoreChannel = (id) =>
  API.patch(`/channels/${id}/restore`);

export const joinChannel = (channelId, userId) =>
  API.post(`/channels/${channelId}/join/${userId}`);

export const leaveChannel = (channelId, userId) =>
  API.post(`/channels/${channelId}/leave/${userId}`);
// ================= WORKSPACE MESSAGES =================

export const createWorkspaceMessage = (data) =>
  API.post("/workspace-messages", data);

export const getWorkspaceMessages = (workspaceId) =>
  API.get(`/workspace-messages/${workspaceId}`);

export const updateWorkspaceMessage = (messageId, data) =>
  API.put(`/workspace-messages/${messageId}`, data);

export const deleteWorkspaceMessage = (messageId, params) =>
  API.delete(`/workspace-messages/${messageId}`, { params });


// ================= CHANNEL MESSAGES =================

export const createChannelMessage = (data) =>
  API.post("/channel-messages", data);

export const getChannelMessages = (channelId) =>
  API.get(`/channel-messages/${channelId}`);


// ================= WORKSPACE TASKS =================

export const createWorkspaceTask = (data) =>
  API.post("/workspace-tasks", data);

export const getWorkspaceTasks = (workspaceId) =>
  API.get(`/workspace-tasks/workspace/${workspaceId}`);


// ================= CHANNEL TASKS =================

export const createChannelTask = (data) =>
  API.post("/channel-tasks", data);

export const getChannelTasks = (channelId) =>
  API.get(`/channel-tasks/channel/${channelId}`);


// ================= TASK DOCUMENTS =================

export const uploadTaskDocument = (formData) =>
  API.post("/task-documents/upload", formData,{
    headers:{
      "Content-Type":"multipart/form-data"
    }
  });

export const getTaskDocuments = (taskId) =>
  API.get(`/task-documents/task/${taskId}`);


// ================= APPROVAL DOCUMENTS =================

export const uploadApprovalDocument = (formData) =>
  API.post("/approval-documents/upload", formData,{
    headers:{
      "Content-Type":"multipart/form-data"
    }
  });

export const getApprovalDocuments = (approvalId) =>
  API.get(`/approval-documents/approval/${approvalId}`);

export default API;
