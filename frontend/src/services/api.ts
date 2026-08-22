const API_URL =
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function getDashboardData() {
    const response = await fetch(`${API_URL}/dashboard`);

    if (!response.ok) {
        throw new Error("Failed to fetch dashboard data");
    }

    return response.json();
}