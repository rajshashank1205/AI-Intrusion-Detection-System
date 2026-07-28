import {
  IconBell,
  IconSearch,
  IconChevronDown,
} from "@tabler/icons-react";

export default function TopNavbar() {
  return (
    <header className="h-20 border-b border-zinc-800 bg-zinc-950 px-8 flex items-center justify-between">

      {/* Search */}

      <div className="relative w-[420px]">

        <IconSearch
          size={18}
          className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500"
        />

        <input
          type="text"
          placeholder="Search alerts, IPs, signatures..."
          className="
            w-full
            h-11
            rounded-lg
            border
            border-zinc-800
            bg-zinc-900
            pl-11
            pr-4
            text-sm
            text-white
            placeholder:text-zinc-500
            outline-none
            transition-all
            focus:border-blue-500
          "
        />

      </div>

      {/* Right Side */}

      <div className="flex items-center gap-6">

        <button className="
          relative
          p-2
          rounded-lg
          hover:bg-zinc-900
          transition
        ">

          <IconBell size={22} className="text-zinc-400" />

          <span className="
            absolute
            top-1
            right-1
            w-2
            h-2
            rounded-full
            bg-red-500
          "/>

        </button>

        <div className="
          h-10
          w-px
          bg-zinc-800
        "/>

        <button className="
          flex
          items-center
          gap-3
          rounded-lg
          px-2
          py-1
          hover:bg-zinc-900
          transition
        ">

          <div className="
            h-10
            w-10
            rounded-full
            bg-blue-600
            flex
            items-center
            justify-center
            font-semibold
            text-white
          ">
            S
          </div>

          <div className="text-left">

            <p className="text-white text-sm font-medium">
              Shashank
            </p>

            <p className="text-xs text-zinc-500">
              Administrator
            </p>

          </div>

          <IconChevronDown
            size={18}
            className="text-zinc-500"
          />

        </button>

      </div>

    </header>
  );
}