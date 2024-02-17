import Image from "next/image";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <div className="z-10 max-w-5xl w-full items-center justify-between lg:flex">
        <span className="font-bold text-3xl">
          Teach me about <span className="text-primary">Linear Algebra</span>
        </span>
      </div>
    </main>
  );
}
