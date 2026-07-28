import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function MainLayout() {
  return (
    <div className="flex h-screen w-screen bg-[var(--background)] text-[var(--text)]">
      <Sidebar />

      <div className="flex flex-1 flex-col overflow-hidden">
        <Topbar />

        <main className="flex-1 overflow-auto p-8">
          <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-10">
            <h1 className="text-3xl font-bold">
              AI Intrusion Detection System
            </h1>

            <p className="mt-3 text-[var(--text-secondary)]">
              Welcome to your cybersecurity dashboard.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}