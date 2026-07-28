interface BadgeProps {
  text: string;
  color?: "green" | "red" | "yellow" | "blue";
}

const colors = {
  green: "bg-green-500/15 text-green-400",
  red: "bg-red-500/15 text-red-400",
  yellow: "bg-yellow-500/15 text-yellow-400",
  blue: "bg-blue-500/15 text-blue-400",
};

export default function Badge({
  text,
  color = "blue",
}: BadgeProps) {
  return (
    <span
      className={`
        px-3
        py-1
        rounded-full
        text-xs
        font-medium
        ${colors[color]}
      `}
    >
      {text}
    </span>
  );
}