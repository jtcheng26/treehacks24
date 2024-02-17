import React from "react";

export default function SecondaryButton({ onClick, children, visible = true }) {
  return (
    <button
      className={
        "border-primary text-primary h-12 rounded-lg text-base hover:brightness-125 transition-all duration-200 flex justify-center items-center " +
        (visible ? "px-4 border-2" : "w-0 border-0")
      }
      onClick={onClick}
    >
      {children}
    </button>
  );
}
