import React from "react";

export default function PrimaryButton({ onClick, children }) {
  return (
    <button className="bg-primary p-2 w-28 rounded-lg font-bold text-xl text-slate-900 hover:scale-110 hover:brightness-110 transition-all duration-200" onClick={onClick}>
      {children}
    </button>
  );
}
