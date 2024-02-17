import { Section } from "@/hooks/useManim";
import React from "react";

export default function ProgressBar({
  active,
  section,
  visible = true,
}: {
  active: boolean;
  section: Section;
  visible: boolean;
}) {
  return (
    <div className="flex flex-col items-center col-span-1 text-sm space-y-1">
      <span
        className="font-bold text-primary transition-all duration-200"
        style={{ opacity: active ? 1 : 0 }}
      >
        {section.title}
      </span>
      <div
        className="bg-slate-700 rounded-full h-2 relative transition-all duration-200"
        style={{ width: visible ? "100%" : "0" }}
      >
        <div
          className="absolute top-0 bottom-0 left-0 right-0 rounded-full bg-primary h-2 transition-all duration-1000 ease-linear"
          style={{ width: section.progressState.played * 100 + "%" }}
        />
      </div>
    </div>
  );
}
