import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import SmoothScroll from "@/components/SmoothScroll";
import { Phone, Mail, MapPin } from "lucide-react";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-display",
});

export const metadata: Metadata = {
  title: "Bhubesi Incorporated | Specialty Services & Engineering",
  description:
    "Bhubesi Incorporated is a luxury engineering and specialty service company. Specialists in air conditioners, cold rooms, mobile kitchens, mobile toilets, and mortuary equipment.",
  keywords:
    "Bhubesi Incorporated, Air Conditioners, Cold Rooms, Body Removal Equipment, Casket Lowering Equipment, Mobile Cold Rooms, Mobile Kitchens, Mobile Toilets, Mortuary Body Lifters, Mortuary Cabinets, Mortuary Fridges, Mortuary Shelves, Mortuary Washing Tables",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable} scroll-smooth`}>
      <body className="antialiased flex flex-col min-h-screen bg-[#f8fafc] text-[#0f172a] selection:bg-[#10b981]/20 selection:text-[#01402c]">
        <SmoothScroll>
          {/* Symmetrical Modern 2026 Header */}
          <header className="sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-slate-100 bg-white/80 backdrop-blur-md transition-luxury">
            <div className="flex items-center gap-3">
              {/* CSS Circle Masking - Crops the raw square logo into a perfect circle to remove the white background corners */}
              <div className="w-10 h-10 rounded-full overflow-hidden border border-emerald-500/20 relative bg-[#022b1d] flex-shrink-0 flex items-center justify-center shadow-sm">
                <img
                  src="/assets/lion_logo_raw.png"
                  alt="Bhubesi Incorporated Circular Lion Logo"
                  className="w-full h-full object-cover object-center select-none scale-[1.05]"
                />
              </div>
              <div className="flex flex-col">
                <span className="font-display font-extrabold text-base md:text-lg tracking-wider text-[#01402c]">
                  BHUBESI
                </span>
                <span className="text-[9px] font-bold tracking-[0.3em] text-[#10b981] uppercase">
                  INCORPORATED
                </span>
              </div>
            </div>

            {/* Desktop Navigation Links */}
            <nav className="hidden md:flex items-center gap-8">
              {[
                { name: "Home", href: "#hero" },
                { name: "About", href: "#about" },
                { name: "Services", href: "#services" },
                { name: "Why Us", href: "#why-choose-us" },
                { name: "Offices", href: "#offices" },
                { name: "Projects", href: "#gallery" },
              ].map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-xs font-semibold tracking-wider text-slate-600 hover:text-[#01402c] uppercase transition-all duration-300 relative group py-1"
                >
                  {item.name}
                  <span className="absolute bottom-0 left-0 w-0 h-[2px] bg-[#10b981] group-hover:w-full transition-all duration-300" />
                </a>
              ))}
            </nav>

            <a
              href="#contact"
              className="px-5 py-2.5 text-xs font-bold tracking-wider text-white bg-[#01402c] hover:bg-[#02573d] rounded-md transition-luxury active:scale-[0.98] uppercase shadow-[0_4px_14px_rgba(1,64,44,0.15)]"
            >
              Enquire
            </a>
          </header>

          {/* Main Content Area */}
          <main className="flex-1 w-full bg-[#f8fafc]">{children}</main>

          {/* Clean 2026 Luxury Deep Forest Green Footer */}
          <footer className="w-full bg-[#012b1d] border-t border-[#01402c] text-slate-300 py-16 px-6 relative overflow-hidden">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
              {/* Brand Column */}
              <div className="flex flex-col gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-full overflow-hidden border border-emerald-500/20 relative bg-[#022b1d] flex-shrink-0 flex items-center justify-center">
                    <img
                      src="/assets/lion_logo_raw.png"
                      alt="Bhubesi Incorporated Logo"
                      className="w-full h-full object-cover select-none scale-[1.05]"
                    />
                  </div>
                  <div className="flex flex-col">
                    <span className="font-display font-extrabold text-lg tracking-wider text-white">
                      BHUBESI
                    </span>
                    <span className="text-[10px] font-semibold tracking-[0.3em] text-[#10b981] uppercase">
                      INCORPORATED
                    </span>
                  </div>
                </div>
                <p className="italic text-[#10b981] font-serif text-sm mt-2">
                  “Where Royalty Meets Excellence”
                </p>
                <p className="text-xs text-slate-400 max-w-sm mt-2 leading-relaxed">
                  Specialists in industrial grade air conditioning, commercial refrigeration, custom mobile assets, and state-of-the-art mortuary equipment designed for extreme reliability and elegance.
                </p>
              </div>

              {/* Quick Links Column */}
              <div className="flex flex-col gap-4 md:pl-12">
                <h4 className="text-sm font-bold tracking-wider text-white uppercase border-b border-[#01402c] pb-2">
                  Quick Navigation
                </h4>
                <ul className="flex flex-col gap-2.5 text-xs font-medium">
                  {[
                    { name: "About Company", href: "#about" },
                    { name: "Services Portfolio", href: "#services" },
                    { name: "Engineering Excellence", href: "#why-choose-us" },
                    { name: "Nationwide Infrastructure", href: "#offices" },
                    { name: "Gallery / Showcase", href: "#gallery" },
                    { name: "Contact Headquarters", href: "#contact" },
                  ].map((item) => (
                    <li key={item.name}>
                      <a
                        href={item.href}
                        className="hover:text-[#10b981] hover:pl-2 transition-all duration-300"
                      >
                        {item.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Contact Information Column */}
              <div className="flex flex-col gap-4">
                <h4 className="text-sm font-bold tracking-wider text-white uppercase border-b border-[#01402c] pb-2">
                  Contact Headquarters
                </h4>
                <ul className="flex flex-col gap-3.5 text-xs text-slate-300">
                  <li className="flex items-start gap-3">
                    <MapPin size={16} className="text-[#10b981] mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="font-bold text-white">Main Office:</p>
                      <p>10 Curran Street, Pietermaritzburg</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <Phone size={16} className="text-[#10b981] mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="font-bold text-white">Call/WhatsApp:</p>
                      <p className="hover:text-[#10b981] transition-colors">073 219 8957</p>
                      <p className="hover:text-[#10b981] transition-colors">078 172 6589</p>
                    </div>
                  </li>
                  <li className="flex items-start gap-3">
                    <Mail size={16} className="text-[#10b981] mt-0.5 flex-shrink-0" />
                    <div>
                      <p className="font-bold text-white">Email Address:</p>
                      <a
                        href="mailto:sales@bhubhesinc.com"
                        className="block hover:text-[#10b981] transition-colors"
                      >
                        sales@bhubhesinc.com
                      </a>
                      <a
                        href="mailto:admin@bhubhesinc.com"
                        className="block hover:text-[#10b981] transition-colors"
                      >
                        admin@bhubhesinc.com
                      </a>
                    </div>
                  </li>
                </ul>
              </div>
            </div>

            <div className="max-w-7xl mx-auto border-t border-[#01402c] mt-12 pt-6 text-center text-xs text-slate-500 flex flex-col md:flex-row justify-between gap-4">
              <p>© {new Date().getFullYear()} Bhubesi Incorporated. All Rights Reserved. Engineered for Royalty.</p>
              <div className="flex justify-center gap-6 text-slate-500">
                <a href="#about" className="hover:text-[#10b981]">Privacy Policy</a>
                <a href="#about" className="hover:text-[#10b981]">Terms of Service</a>
              </div>
            </div>
          </footer>
        </SmoothScroll>
      </body>
    </html>
  );
}
