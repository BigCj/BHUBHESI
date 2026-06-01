"use client";

import React from "react";

interface LionLogoProps {
  className?: string;
  size?: number;
  variant?: "white" | "gold" | "emerald";
  glow?: boolean;
}

export default function LionLogo({
  className = "",
  size = 64,
  variant = "white",
  glow = false,
}: LionLogoProps) {
  // Define fills and gradients based on the requested theme
  const getColors = () => {
    switch (variant) {
      case "gold":
        return {
          stroke: "url(#gold-gradient-logo)",
          fill: "url(#gold-gradient-logo)",
          accent: "#f7e3af",
        };
      case "emerald":
        return {
          stroke: "#0d4d38",
          fill: "#022b1d",
          accent: "#cfa84a",
        };
      case "white":
      default:
        return {
          stroke: "#ffffff",
          fill: "#ffffff",
          accent: "#cfa84a",
        };
    }
  };

  const colors = getColors();

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`${className} transition-luxury ${
        glow ? "drop-shadow-[0_0_15px_rgba(207,168,74,0.4)]" : ""
      }`}
    >
      <defs>
        {/* Luxury multi-stop gold gradient for the royal look */}
        <linearGradient id="gold-gradient-logo" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#aa771c" />
          <stop offset="30%" stopColor="#f7e3af" />
          <stop offset="70%" stopColor="#cfa84a" />
          <stop offset="100%" stopColor="#f7e3af" />
        </linearGradient>
      </defs>

      {/* Symmetrical Outer Border Circle (optional premium casing) */}
      <circle
        cx="100"
        cy="100"
        r="94"
        stroke={colors.stroke}
        strokeWidth="2.5"
        strokeDasharray="4 4"
        className="opacity-40 animate-[spin_120s_linear_infinite]"
      />
      <circle
        cx="100"
        cy="100"
        r="88"
        stroke={colors.stroke}
        strokeWidth="1.5"
        className="opacity-70"
      />

      {/* The Symmetrical Forward-Facing Lion Head Vector */}
      <g id="lion-head" stroke={colors.stroke} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" fill="none">
        {/* Outer Symmetrical Mane Tufts */}
        <path d="M100 28 C75 35 55 45 42 62 C32 75 28 92 31 108 C34 125 45 140 60 152 C70 160 85 167 100 170" />
        <path d="M100 28 C125 35 145 45 158 62 C168 75 172 92 169 108 C166 125 155 140 140 152 C130 160 115 167 100 170" />

        {/* Second Layer of Mane (Flame-like Flowing Locks) */}
        <path d="M52 70 C45 85 45 105 52 120 C58 132 70 145 84 153" />
        <path d="M148 70 C155 85 155 105 148 120 C142 132 130 145 116 153" />

        <path d="M64 78 C59 90 59 108 66 120 C72 130 82 138 94 142" />
        <path d="M136 78 C141 90 141 108 134 120 C128 130 118 138 106 142" />

        {/* Top Brow Crown Mane Elements */}
        <path d="M80 48 C80 38 90 32 100 32 C110 32 120 38 120 48" />
        <path d="M88 56 C88 48 94 44 100 44 C106 44 112 48 112 56" />

        {/* Symmetrical Ears */}
        <path d="M52 68 C40 64 36 50 48 44 C56 40 66 48 68 56" />
        <path d="M148 68 C160 64 164 50 152 44 C144 40 134 48 132 56" />
        
        {/* Inner ear details */}
        <path d="M50 56 C44 54 44 48 50 48" />
        <path d="M150 56 C156 54 156 48 150 48" strokeWidth="2" />

        {/* Face Outline & Cheekbones */}
        <path d="M72 90 C72 75 80 68 100 68 C120 68 128 75 128 90 C128 102 122 110 115 115 C108 120 100 120 100 120" />
        <path d="M72 90 C72 102 78 110 85 115 C92 120 100 120 100 120" />

        {/* Symmetrical Majestic Eyebrows */}
        <path d="M78 84 C85 82 92 84 96 90" strokeWidth="3.5" />
        <path d="M122 84 C115 82 108 84 104 90" strokeWidth="3.5" />

        {/* Symmetrical Royal Eyes */}
        <path d="M80 92 C83 89 89 89 92 92 C89 95 83 95 80 92 Z" fill={colors.fill} />
        <path d="M120 92 C117 89 111 89 108 92 C111 95 117 95 120 92 Z" fill={colors.fill} />
        
        {/* Eye Pupils */}
        <circle cx="86" cy="92" r="1.5" fill={colors.accent} stroke="none" />
        <circle cx="114" cy="92" r="1.5" fill={colors.accent} stroke="none" />

        {/* Strong Majestic Nose Bridge and Muzzle */}
        <path d="M96 90 L94 112 C94 118 97 122 100 122 C103 122 106 118 106 112 L104 90" />
        {/* Nose Tip (V-shaped) */}
        <path d="M92 112 H108 L100 120 Z" fill={colors.fill} />

        {/* Royal Whisker Pads & Mouth (Muzzle Bulbs) */}
        <path d="M100 122 C94 122 86 126 86 134 C86 142 94 146 100 146 C106 146 114 142 114 134 C114 126 106 122 100 122" />
        
        {/* Mouth Center Line */}
        <path d="M100 122 V132" strokeWidth="2.5" />
        
        {/* Symmetrical Chin (Beard) */}
        <path d="M88 140 C92 152 100 156 100 156 C100 156 108 152 112 140" strokeWidth="3" />
        
        {/* Whisker Dot Details */}
        <circle cx="91" cy="132" r="1" fill={colors.stroke} stroke="none" />
        <circle cx="95" cy="135" r="1" fill={colors.stroke} stroke="none" />
        <circle cx="91" cy="138" r="1" fill={colors.stroke} stroke="none" />
        
        <circle cx="109" cy="132" r="1" fill={colors.stroke} stroke="none" />
        <circle cx="105" cy="135" r="1" fill={colors.stroke} stroke="none" />
        <circle cx="109" cy="138" r="1" fill={colors.stroke} stroke="none" />

        {/* Majestic Forehead Marks */}
        <path d="M100 52 V64" strokeWidth="2" />
        <path d="M94 56 L100 62 L106 56" strokeWidth="2" />
      </g>
    </svg>
  );
}
