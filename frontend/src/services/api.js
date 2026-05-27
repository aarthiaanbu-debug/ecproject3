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
  API.get(`/comment/${task_id}`);

export const addComment = (data) =>
  API.post("/comment/create", null, {
    params: data,
  });


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

export const createStripeSession = (plan) =>
  API.post("/stripe/create-checkout-session", { plan });

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

export default API;
