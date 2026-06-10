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

export default API;