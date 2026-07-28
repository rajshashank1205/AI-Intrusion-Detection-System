import type { ReactNode } from "react";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export default function Card({
  children,
  className = "",
}: CardProps) {
  return (
    <div
      className={`
        rounded-2xl
        border
        border-zinc-800
        bg-zinc-950/70
        backdrop-blur-md
        shadow-lg
        p-6
        transition-all
        duration-200
        hover:border-zinc-700
        ${className}
      `}
    >
      {children}
    </div>
  );
} 