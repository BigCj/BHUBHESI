"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Wind,
  Snowflake,
  Activity,
  ArrowDownCircle,
  Truck,
  ChefHat,
  Sparkles,
  Users,
  Compass,
  Phone,
  Mail,
  MapPin,
  CheckCircle2,
  ChevronRight,
  Clock,
  ArrowRight,
  Shield,
  Briefcase,
  Layers,
} from "lucide-react";

// The 12 specialized services grouped elegantly for 2026 elite scannability
const serviceGroups = [
  {
    title: "Air & Thermal Control Systems",
    description: "State-of-the-art climate engineering for premium comfort and commercial operations.",
    services: [
      {
        name: "Air Conditioners",
        desc: "Advanced industrial, corporate, and residential HVAC setups engineered for heavy-duty climate control.",
        icon: Wind,
      },
      {
        name: "Cold Rooms",
        desc: "Custom-built, temperature-regulated walk-in cold rooms for storage, catering, and logistics.",
        icon: Snowflake,
      },
      {
        name: "Mobile Cold Rooms",
        desc: "Robust, heavy-duty mobile refrigeration trailers designed to preserve perishables on the move.",
        icon: Truck,
      },
    ],
  },
  {
    title: "Premium Mortuary Equipment",
    description: "Highly specialized, sanitary, and dignified engineering solutions for the healthcare sector.",
    services: [
      {
        name: "Mortuary Cabinets",
        desc: "Premium Grade 304 stainless steel cabinets with independent cooling modules and ergonomic sliding racks.",
        icon: Compass,
      },
      {
        name: "Mortuary Fridges",
        desc: "Advanced refrigeration systems with digital temperature tracking, backup alarms, and multi-bay layouts.",
        icon: Snowflake,
      },
      {
        name: "Mortuary Shelves",
        desc: "Heavy-duty structural storage racks crafted from anti-corrosive stainless steel for severe operations.",
        icon: Compass,
      },
      {
        name: "Mortuary Washing Tables",
        desc: "Ergonomically designed sanitation stations equipped with built-in drainage, wash sprays, and waste disposals.",
        icon: Activity,
      },
      {
        name: "Mortuary Body Lifters",
        desc: "Hydraulic and electric power-assisted lifters engineered for safe, smooth, and dignified body handling.",
        icon: ArrowDownCircle,
      },
      {
        name: "Body Removal Equipment",
        desc: "Heavy-duty, quiet-operating trolleys, stretchers, and transport setups optimized for luxury service teams.",
        icon: Activity,
      },
      {
        name: "Casket Lowering Equipment",
        desc: "Precision mechanical lowering gears designed for silent, smooth, and ultra-reliable operations during services.",
        icon: ArrowDownCircle,
      },
    ],
  },
  {
    title: "Custom Mobile Assets",
    description: "Bespoke service units designed to deliver luxury food service and amenities anywhere in the country.",
    services: [
      {
        name: "Mobile Kitchens",
        desc: "Gourmet, restaurant-grade mobile kitchens complete with stainless gas fixtures, prep tables, and extractors.",
        icon: ChefHat,
      },
      {
        name: "Mobile Toilets",
        desc: "Sleek, luxury VIP mobile sanitation cabins featuring self-cleaning technology and premium amenities.",
        icon: Sparkles,
      },
    ],
  },
];

// Why Choose Us statistics and columns
const whyChooseUsData = [
  {
    title: "Nationwide Infrastructure",
    value: "100%",
    desc: "Active logistics, delivery, and technician dispatch nationwide across South Africa.",
    icon: Compass,
  },
  {
    title: "Premium & Affordable Options",
    value: "Grade 304 & Galvanised",
    desc: "Crafted from elite Grade 304 Stainless Steel or highly durable, cost-effective Galvanised Steel to match any budget.",
    icon: Shield,
  },
  {
    title: "Elite Support & Servicing",
    value: "24/7 Support",
    desc: "Round-the-clock emergency support and preventative maintenance for continuous operations.",
    icon: Clock,
  },
  {
    title: "Customer Satisfaction",
    value: "100% Trust",
    desc: "Corporate complexes, hospitals, and specialty service entities supplied with pride.",
    icon: Users,
  },
];

export default function Homepage() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [formSubmitted, setFormSubmitted] = useState(false);

  // Gallery items referencing the uploaded images
  const galleryItems = [
    {
      src: "/assets/flyer.jpg",
      title: "Bhubesi Services Flyer",
      subtitle: "Green & Gold Theme",
    },
    {
      src: "/assets/poster.jpg",
      title: "Trusted Engineering Poster",
      subtitle: "White Details Guide",
    },
  ];

  return (
    <div className="w-full relative bg-[#f8fafc] text-[#0f172a]">
      {/* ========================================================================= */}
      {/* 1. HERO SECTION: Minimalist 2026 Spacious Green Corporate Grid             */}
      {/* ========================================================================= */}
      <section id="hero" className="relative w-full py-20 md:py-32 px-6 bg-gradient-to-b from-[#eef7f4] via-[#f8fafc] to-[#f8fafc] overflow-hidden">
        {/* Subtle geometric line patterns for 2026 modern tech feel */}
        <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: "radial-gradient(#01402c 1.5px, transparent 1.5px)", backgroundSize: "24px 24px" }} />

        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          {/* Left Column: Heading and CTAs (lg:col-span-7) */}
          <div className="lg:col-span-7 flex flex-col gap-6 items-start">
            {/* Minimalist Mint Slogan Badge */}
            <div className="px-3.5 py-1.5 rounded-full border border-emerald-500/10 bg-emerald-500/5 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#10b981]" />
              <span className="text-[10px] font-bold tracking-[0.2em] text-[#059669] uppercase">
                Where Royalty Meets Excellence
              </span>
            </div>

            {/* Symmetrical Spacious Typography */}
            <div className="flex flex-col gap-2">
              <h1 className="font-display font-black text-4xl sm:text-6xl tracking-tight text-[#01402c] leading-[1.05] uppercase">
                BHUBESI
              </h1>
              <h2 className="text-lg sm:text-xl font-bold tracking-[0.25em] text-[#10b981] uppercase">
                INCORPORATED
              </h2>
            </div>

            <p className="text-slate-600 text-sm sm:text-base max-w-xl leading-relaxed font-normal">
              South Africa’s premier luxury engineering and specialty service company. Providing gold-standard environmental solutions and custom mortuary assets for corporate, medical, and public structures nationwide.
            </p>

            {/* Clean, minimalist call to action buttons */}
            <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto mt-4">
              <a
                href="#services"
                className="px-8 py-3.5 text-xs font-bold tracking-wider text-white bg-[#01402c] hover:bg-[#02573d] transition-luxury rounded-md uppercase text-center shadow-[0_4px_14px_rgba(1,64,44,0.15)]"
              >
                Our Portfolios
              </a>
              <a
                href="#about"
                className="px-8 py-3.5 text-xs font-bold tracking-wider text-[#01402c] border border-slate-200 hover:bg-slate-50 transition-luxury rounded-md uppercase text-center"
              >
                About The Incorporated
              </a>
            </div>
          </div>

          {/* Right Column: Premium Dashboard Card with flyer (lg:col-span-5) */}
          <div className="lg:col-span-5 relative flex justify-center items-center">
            {/* The main flyer picture frame */}
            <div className="luxury-card p-4 rounded-xl relative z-10 w-full max-w-sm shadow-xl group border border-slate-100">
              <div className="absolute top-6 right-6 bg-[#01402c] px-3 py-1 rounded-full border border-emerald-500/20 text-[9px] font-bold tracking-wider text-white uppercase">
                Specialty Services
              </div>

              <div className="overflow-hidden border border-slate-100 rounded-lg">
                <img
                  src="/assets/flyer.jpg"
                  alt="Bhubesi Incorporated Emerald Flyer"
                  className="w-full h-auto object-cover group-hover:scale-[1.03] transition-all duration-500"
                />
              </div>
              <div className="mt-4 flex justify-between items-center px-1">
                <div>
                  <h4 className="text-xs font-bold uppercase text-[#01402c] tracking-wider">
                    Official Brochure
                  </h4>
                  <p className="text-[10px] text-slate-400">Pietermaritzburg HQ catalogs</p>
                </div>
                <a
                  href="#gallery"
                  className="p-2 rounded-full border border-slate-100 text-[#01402c] hover:bg-[#01402c] hover:text-white transition-luxury"
                >
                  <ChevronRight size={14} />
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 2. ABOUT SECTION: Brand Identity & Product Showcase Frame                */}
      {/* ========================================================================= */}
      <section id="about" className="relative w-full py-28 px-6 bg-white overflow-hidden border-t border-slate-50">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Column: Copy */}
          <div className="flex flex-col gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-[2px] bg-[#10b981]" />
              <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
                ESTABLISHED FOR ROYALTY
              </span>
            </div>

            <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase leading-tight">
              A LEADER IN SPECIALTY ENGINEERING SERVICES
            </h3>

            <p className="text-slate-600 text-sm leading-relaxed">
              Bhubesi Incorporated stands as South Africa’s premier elite manufacturer and servicing giant. Combining heavy industrial durability with elegant corporate finishing, we serve national hospitals, premium dining venues, municipalities, and private service directors with custom systems designed for supreme reliability.
            </p>

            <p className="text-slate-500 text-xs md:text-sm leading-relaxed font-light">
              Every asset carrying the forward-facing white lion head is hand-inspected, precision-welded with Grade 304 anti-microbial stainless steels, and fitted with certified hermetic systems. We operate with a strict nation-wide servicing standard ensuring our air controllers, specialized mortuary equipment, and high-end mobile VIP facilities perform tirelessly under extreme stress.
            </p>

            {/* Quick trust metrics */}
            <div className="grid grid-cols-2 gap-6 mt-4">
              <div className="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
                <div className="flex items-center gap-2 text-[#01402c] mb-1">
                  <CheckCircle2 size={16} className="text-[#10b981]" />
                  <span className="text-xs font-bold uppercase tracking-wider">Premium Build</span>
                </div>
                <p className="text-xs text-slate-500 leading-normal font-light">
                  Anti-corrosive, medical grade metals for superior hygiene and structural durability.
                </p>
              </div>

              <div className="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
                <div className="flex items-center gap-2 text-[#01402c] mb-1">
                  <CheckCircle2 size={16} className="text-[#10b981]" />
                  <span className="text-xs font-bold uppercase tracking-wider">National Network</span>
                </div>
                <p className="text-xs text-slate-500 leading-normal font-light">
                  Active technicians and rapid emergency services deployed 24/7 in every province.
                </p>
              </div>
            </div>
          </div>

          {/* Right Column: Premium Framed Artwork (Displaying the Real Flyers) */}
          <div className="relative flex justify-center items-center">
            {/* The main flyer picture frame */}
            <div className="luxury-card p-4 rounded-xl relative z-10 w-full max-w-sm shadow-xl group border border-slate-100">
              <div className="absolute top-6 right-6 bg-[#10b981] px-3 py-1 rounded-full border border-emerald-500/20 text-[9px] font-bold tracking-wider text-white uppercase">
                Product Guide
              </div>

              <div className="overflow-hidden border border-slate-100 rounded-lg">
                <img
                  src="/assets/poster.jpg"
                  alt="Bhubesi Incorporated White Poster"
                  className="w-full h-auto object-cover group-hover:scale-[1.03] transition-all duration-500"
                />
              </div>
              <div className="mt-4 flex justify-between items-center px-1">
                <div>
                  <h4 className="text-xs font-bold uppercase text-[#01402c] tracking-wider">
                    Corporate Catalog
                  </h4>
                  <p className="text-[10px] text-slate-400">Trusted Experts Guide</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 3. SERVICES SECTION: The 12 Specialized Products Grouped                  */}
      {/* ========================================================================= */}
      <section id="services" className="relative w-full py-28 px-6 bg-[#f8fafc] border-t border-slate-100">
        {/* Symmetrical Header */}
        <div className="max-w-7xl mx-auto flex flex-col items-center text-center gap-4 mb-20">
          <div className="flex items-center gap-2 justify-center">
            <div className="w-6 h-[2px] bg-[#10b981]" />
            <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
              OUR ENGINEERING SPECIFICITY
            </span>
            <div className="w-6 h-[2px] bg-[#10b981]" />
          </div>

          <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase">
            INDUSTRIAL & SPECIALTY SERVICES
          </h3>

          <p className="text-slate-500 text-sm max-w-2xl font-light">
            Clearly presenting our engineered product lines, built for durability and refined styling. Check out our 12 specialized portfolios below:
          </p>
        </div>

        {/* The Grouped Grid */}
        <div className="max-w-7xl mx-auto flex flex-col gap-20">
          {serviceGroups.map((group, gIdx) => (
            <div key={group.title} className="flex flex-col gap-8">
              {/* Group Label */}
              <div className="flex flex-col gap-2 border-b border-slate-200 pb-4">
                <div className="flex items-center justify-between">
                  <h4 className="font-display font-bold text-xl md:text-2xl text-[#01402c] tracking-wider uppercase">
                    {group.title}
                  </h4>
                  <span className="text-[10px] font-bold text-slate-400 tracking-wider">
                    PORTFOLIO 0{gIdx + 1}
                  </span>
                </div>
                <p className="text-xs text-slate-500 max-w-xl font-light">
                  {group.description}
                </p>
              </div>

              {/* Service Cards Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {group.services.map((service) => {
                  const Icon = service.icon;
                  return (
                    <div
                      key={service.name}
                      className="luxury-card p-8 rounded-xl flex flex-col justify-between gap-6"
                    >
                      <div className="flex flex-col gap-4">
                        {/* Mint Glowing Icon Container */}
                        <div className="w-12 h-12 rounded-lg bg-emerald-50 text-[#10b981] flex items-center justify-center shadow-sm">
                          <Icon size={22} className="stroke-[1.5]" />
                        </div>

                        <div className="flex flex-col gap-1.5">
                          <h5 className="font-display font-bold text-sm md:text-base text-[#01402c] tracking-wider uppercase">
                            {service.name}
                          </h5>
                          <p className="text-xs text-slate-500 leading-relaxed font-light">
                            {service.desc}
                          </p>
                        </div>
                      </div>

                      <a
                        href="#contact"
                        className="flex items-center gap-1.5 text-[10px] font-bold tracking-wider text-[#10b981] hover:text-[#01402c] uppercase transition-colors"
                      >
                        Enquire Specifications <ArrowRight size={12} className="mt-0.5" />
                      </a>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 4. WHY CHOOSE US: Modern Benchmarks & Metrics                             */}
      {/* ========================================================================= */}
      <section id="why-choose-us" className="relative w-full py-28 px-6 bg-white border-t border-slate-100">
        <div className="max-w-7xl mx-auto flex flex-col lg:flex-row gap-16 items-center">
          {/* Copy Column */}
          <div className="flex flex-col gap-6 lg:w-1/3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-[2px] bg-[#10b981]" />
              <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
                THE BHUBESI BENCHMARK
              </span>
            </div>

            <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase leading-tight">
              WHY ROYALTY CHOOSE US
            </h3>

            <p className="text-slate-600 text-xs md:text-sm leading-relaxed font-light">
              We do not build average products. Bhubesi Incorporated was established to serve demanding industries that require zero downtime, anti-microbial environments, and seamless mobility. We serve clients who value elite craftsmanship.
            </p>

            <a
              href="#contact"
              className="px-6 py-3 border border-[#01402c] text-[#01402c] hover:bg-slate-50 transition-luxury text-xs font-bold tracking-wider rounded-md uppercase w-fit"
            >
              Request Custom Blueprint
            </a>
          </div>

          {/* Stats Grid Column */}
          <div className="lg:w-2/3 grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
            {whyChooseUsData.map((stat) => {
              const Icon = stat.icon;
              return (
                <div
                  key={stat.title}
                  className="luxury-card p-8 rounded-xl flex flex-col gap-4 relative group"
                >
                  <div className="flex items-center justify-between">
                    <div className="w-10 h-10 rounded-lg bg-emerald-50 text-[#10b981] flex items-center justify-center">
                      <Icon size={18} />
                    </div>
                    <span className="font-display font-black text-xl md:text-2xl text-[#01402c] tracking-tight">
                      {stat.value}
                    </span>
                  </div>

                  <div className="flex flex-col gap-1">
                    <h4 className="text-xs font-bold tracking-wider text-[#01402c] uppercase">
                      {stat.title}
                    </h4>
                    <p className="text-[11px] text-slate-500 leading-relaxed font-light">
                      {stat.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 5. NATIONWIDE OFFICES: Headquarters and Branches                          */}
      {/* ========================================================================= */}
      <section id="offices" className="relative w-full py-28 px-6 bg-[#f8fafc] border-t border-slate-100">
        <div className="max-w-7xl mx-auto flex flex-col items-center text-center gap-4 mb-20">
          <div className="flex items-center gap-2 justify-center">
            <div className="w-6 h-[2px] bg-[#10b981]" />
            <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
              OUR SERVICE FOOTPRINT
            </span>
            <div className="w-6 h-[2px] bg-[#10b981]" />
          </div>

          <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase">
            NATIONWIDE OFFICES & SUPPLY INFRASTRUCTURE
          </h3>

          <p className="text-slate-500 text-sm max-w-2xl font-light">
            Operating from our primary manufacturing and distribution headquarters in KwaZulu-Natal, with support hubs covering all metropolitan zones.
          </p>
        </div>

        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* PIETERMARITZBURG HEADQUARTERS CARD (HIGHLIGHTED IN EMERALD) */}
          <div className="lg:col-span-2 border border-emerald-500/20 bg-white p-8 md:p-12 rounded-xl relative overflow-hidden shadow-sm flex flex-col justify-between gap-8 group">
            {/* Absolute background accent */}
            <div className="absolute top-0 right-0 w-80 h-80 bg-emerald-500/5 rounded-full blur-[80px] pointer-events-none" />

            <div className="flex flex-col gap-6 relative z-10">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-14 h-14 rounded-full overflow-hidden border border-emerald-500/20 relative bg-[#022b1d] flex-shrink-0 flex items-center justify-center shadow-sm">
                    <img
                      src="/assets/lion_logo_raw.png"
                      alt="Bhubesi Incorporated Logo"
                      className="w-full h-full object-cover select-none scale-[1.05]"
                    />
                  </div>
                  <div className="flex flex-col">
                    <span className="font-display font-extrabold text-lg tracking-wider text-[#01402c]">
                      BHUBESI HQ
                    </span>
                    <span className="text-[9px] font-semibold tracking-[0.25em] text-[#10b981] uppercase">
                      PIETERMARITZBURG PRIMARY
                    </span>
                  </div>
                </div>
                <span className="px-3.5 py-1 bg-emerald-50 border border-emerald-500/20 text-[#059669] text-[9px] font-bold tracking-wider uppercase rounded-md w-fit">
                  Central Manufacturing Hub
                </span>
              </div>

              <div className="w-full h-[1px] bg-slate-100" />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 text-xs text-slate-600">
                <div className="flex flex-col gap-3">
                  <p className="font-bold text-[#01402c] uppercase tracking-wider">Physical Address</p>
                  <div className="flex items-start gap-2.5 text-slate-800">
                    <MapPin size={16} className="text-[#10b981] flex-shrink-0" />
                    <span>10 Curran Street, Pietermaritzburg, South Africa</span>
                  </div>
                  <p className="text-[11px] text-slate-400 font-light">
                    Direct access for fleet pickup, client inspections, and commercial collections.
                  </p>
                </div>

                <div className="flex flex-col gap-3">
                  <p className="font-bold text-[#01402c] uppercase tracking-wider">Direct Channels</p>
                  <div className="flex flex-col gap-2">
                    <div className="flex items-center gap-2.5 text-slate-800">
                      <Phone size={14} className="text-[#10b981]" />
                      <span>073 219 8957 (WhatsApp)</span>
                    </div>
                    <div className="flex items-center gap-2.5 text-slate-800">
                      <Phone size={14} className="text-[#10b981]" />
                      <span>078 172 6589 (Service)</span>
                    </div>
                    <div className="flex items-center gap-2.5 text-slate-800">
                      <Mail size={14} className="text-[#10b981]" />
                      <a href="mailto:sales@bhubhesinc.com" className="hover:underline">
                        sales@bhubhesinc.com
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <a
              href="#contact"
              className="w-full text-center py-4 bg-[#01402c] hover:bg-[#02573d] transition-luxury font-bold tracking-wider text-white text-xs uppercase rounded-md mt-4 z-10 relative shadow-[0_4px_14px_rgba(1,64,44,0.15)]"
            >
              Schedule an On-Site Blueprint Session
            </a>
          </div>

          {/* SATELLITE DISPATCH CENTERS */}
          <div className="luxury-card p-8 rounded-xl flex flex-col justify-between gap-6 relative">
            <div className="flex flex-col gap-4">
              <span className="text-[10px] font-bold text-slate-400 tracking-wider">BRANCH LOGISTICS</span>
              <h4 className="font-display font-bold text-base md:text-lg text-[#01402c] tracking-wider uppercase">
                METROPOLITAN HUBS
              </h4>
              <p className="text-xs text-slate-500 leading-relaxed font-light mb-2">
                Operational hubs offering localized maintenance, stock delivery, and technical consulting:
              </p>

              <ul className="flex flex-col gap-4 text-xs">
                {[
                  { city: "Durban Service Hub", area: "Pinetown Industrial Zone" },
                  { city: "Johannesburg Logistics", area: "Sandton Complex & City Deep" },
                  { city: "Cape Town Dispatch", area: "Paarden Eiland Hub" },
                  { city: "Gqeberha Maintenance", area: "Coega Port Support" },
                ].map((hub) => (
                  <li key={hub.city} className="flex flex-col gap-0.5 border-l-2 border-[#10b981] pl-3">
                    <span className="font-bold text-slate-800 uppercase">{hub.city}</span>
                    <span className="text-[10px] text-slate-400 font-light">{hub.area}</span>
                  </li>
                ))}
              </ul>
            </div>

            <span className="text-[9px] italic text-slate-400">
              *All client orders are dispatched from the primary Pietermaritzburg facility.
            </span>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 6. GALLERY & PROJECT CASE STUDIES: Flyer & Poster Display                 */}
      {/* ========================================================================= */}
      <section id="gallery" className="relative w-full py-28 px-6 bg-white border-t border-slate-100 overflow-hidden">
        <div className="max-w-7xl mx-auto flex flex-col items-center text-center gap-4 mb-20">
          <div className="flex items-center gap-2 justify-center">
            <div className="w-6 h-[2px] bg-[#10b981]" />
            <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
              THE BRAND GALLERY
            </span>
            <div className="w-6 h-[2px] bg-[#10b981]" />
          </div>

          <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase">
            CORPORATE CATALOGS & PORTFOLIO IMAGES
          </h3>

          <p className="text-slate-500 text-sm max-w-2xl font-light">
            Inspect our high-end marketing, project details, and corporate visual designs as seen in our official brand materials. Click to zoom on any asset.
          </p>
        </div>

        {/* Catalog Grid */}
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 justify-center">
          {galleryItems.map((item) => (
            <div
              key={item.src}
              onClick={() => setSelectedImage(item.src)}
              className="luxury-card p-3 rounded-xl cursor-pointer shadow-sm relative overflow-hidden max-w-md mx-auto"
            >
              {/* Image Frame Container */}
              <div className="overflow-hidden rounded-lg relative aspect-[4/3] border border-slate-100 bg-slate-50">
                <img
                  src={item.src}
                  alt={item.title}
                  className="w-full h-full object-contain p-2 group-hover:scale-[1.03] transition-all duration-500"
                />
                {/* Floating view lens */}
                <div className="absolute inset-0 bg-emerald-950/60 opacity-0 hover:opacity-100 flex items-center justify-center transition-all duration-300 pointer-events-none">
                  <span className="px-4 py-2 border border-[#10b981] text-[#10b981] text-[10px] tracking-wider uppercase font-bold bg-[#01402c] rounded-md">
                    Inspect Catalog
                  </span>
                </div>
              </div>

              <div className="mt-4 px-1 flex flex-col gap-0.5">
                <h4 className="text-xs font-bold uppercase text-[#01402c] tracking-wider">
                  {item.title}
                </h4>
                <p className="text-[10px] text-slate-400">{item.subtitle}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Modal Lightbox for Premium Asset Inspection */}
        <AnimatePresence>
          {selectedImage && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSelectedImage(null)}
              className="fixed inset-0 bg-[#012b1d]/95 z-[100] flex items-center justify-center p-4 md:p-8 cursor-zoom-out"
            >
              <motion.div
                initial={{ scale: 0.95 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.95 }}
                className="relative max-w-4xl max-h-[90vh] bg-white p-2 rounded-xl shadow-2xl border border-slate-100"
              >
                <img
                  src={selectedImage}
                  alt="Expanded Asset Catalog Showcase"
                  className="max-w-full max-h-[85vh] object-contain rounded-lg"
                />
                <button
                  onClick={() => setSelectedImage(null)}
                  className="absolute top-4 right-4 bg-[#01402c] text-white px-3.5 py-1.5 rounded-full text-[9px] font-bold tracking-wider uppercase shadow-md hover:bg-[#02573d]"
                >
                  Close Catalog
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </section>

      {/* ========================================================================= */}
      {/* 7. CONTACT SECTION: Luxury Inquiry Form & Direct Communication           */}
      {/* ========================================================================= */}
      <section id="contact" className="relative w-full py-28 px-6 bg-[#f8fafc] border-t border-slate-100">
        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">
          {/* Left Column: Contact details */}
          <div className="flex flex-col gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-[2px] bg-[#10b981]" />
              <span className="text-xs font-bold tracking-widest text-[#10b981] uppercase">
                GET IN TOUCH
              </span>
            </div>

            <h3 className="font-display font-extrabold text-3xl md:text-5xl tracking-tight text-[#01402c] uppercase leading-tight">
              CONNECT WITH OUR ELITE ENGINEERS
            </h3>

            <p className="text-slate-600 text-xs md:text-sm leading-relaxed font-light">
              Do you have a specific commercial complex, healthcare facility, or VIP mobile project requiring customized specifications? Submit your details directly to our corporate offices, or contact us using our direct channels:
            </p>

            <div className="flex flex-col gap-4 mt-4">
              <div className="flex items-start gap-4 p-5 border border-slate-150 bg-white rounded-lg shadow-sm">
                <Phone className="text-[#10b981] mt-0.5 flex-shrink-0" size={20} />
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-[#01402c] tracking-wider uppercase">
                    WhatsApp & Main Line
                  </span>
                  <a href="tel:0732198957" className="text-sm font-bold text-slate-800 hover:text-[#10b981] transition-colors mt-0.5">
                    073 219 8957
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4 p-5 border border-slate-155 bg-white rounded-lg shadow-sm">
                <Mail className="text-[#10b981] mt-0.5 flex-shrink-0" size={20} />
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-[#01402c] tracking-wider uppercase">
                    Technical Sales
                  </span>
                  <a href="mailto:sales@bhubhesinc.com" className="text-sm font-bold text-slate-800 hover:text-[#10b981] transition-colors mt-0.5">
                    sales@bhubhesinc.com
                  </a>
                </div>
              </div>

              <div className="flex items-start gap-4 p-5 border border-slate-155 bg-white rounded-lg shadow-sm">
                <Mail className="text-[#10b981] mt-0.5 flex-shrink-0" size={20} />
                <div className="flex flex-col">
                  <span className="text-[10px] font-bold text-[#01402c] tracking-wider uppercase">
                    Operations & Admin
                  </span>
                  <a href="mailto:admin@bhubhesinc.com" className="text-sm font-bold text-slate-800 hover:text-[#10b981] transition-colors mt-0.5">
                    admin@bhubhesinc.com
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Premium Form */}
          <div className="luxury-card p-8 md:p-12 rounded-xl shadow-xl relative border border-slate-100 bg-white">
            <h4 className="font-display font-bold text-lg md:text-xl text-[#01402c] tracking-wider uppercase mb-6">
              CORPORATE INQUIRY FORM
            </h4>

            {formSubmitted ? (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="py-12 flex flex-col items-center text-center gap-4"
              >
                <div className="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-500/20 flex items-center justify-center text-[#10b981] mb-2 shadow-sm">
                  <CheckCircle2 size={32} />
                </div>
                <h5 className="font-display font-bold text-base text-[#01402c] tracking-wider uppercase">
                  Inquiry Dispatched Successfully
                </h5>
                <p className="text-xs text-slate-500 max-w-sm leading-relaxed font-light">
                  Our specialty engineering dispatch team will review your specifications and contact your office within two business hours.
                </p>
                <button
                  onClick={() => setFormSubmitted(false)}
                  className="mt-6 text-xs text-[#10b981] hover:text-[#01402c] underline font-bold tracking-wider uppercase"
                >
                  Submit Another Specification
                </button>
              </motion.div>
            ) : (
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  setFormSubmitted(true);
                }}
                className="flex flex-col gap-5 text-xs text-slate-700"
              >
                <div className="flex flex-col gap-2">
                  <label htmlFor="companyName" className="font-bold text-slate-500 uppercase tracking-wider">
                    Company Name
                  </label>
                  <input
                    required
                    type="text"
                    id="companyName"
                    className="w-full bg-[#f8fafc] border border-slate-200 focus:border-[#10b981] px-4 py-3 rounded-md focus:outline-none transition-luxury"
                    placeholder="Enter your registered company"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex flex-col gap-2">
                    <label htmlFor="clientName" className="font-bold text-slate-500 uppercase tracking-wider">
                      Representative Name
                    </label>
                    <input
                      required
                      type="text"
                      id="clientName"
                      className="w-full bg-[#f8fafc] border border-slate-200 focus:border-[#10b981] px-4 py-3 rounded-md focus:outline-none transition-luxury"
                      placeholder="Enter full name"
                    />
                  </div>

                  <div className="flex flex-col gap-2">
                    <label htmlFor="clientEmail" className="font-bold text-slate-500 uppercase tracking-wider">
                      Corporate Email
                    </label>
                    <input
                      required
                      type="email"
                      id="clientEmail"
                      className="w-full bg-[#f8fafc] border border-slate-200 focus:border-[#10b981] px-4 py-3 rounded-md focus:outline-none transition-luxury"
                      placeholder="name@company.com"
                    />
                  </div>
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="interest" className="font-bold text-slate-500 uppercase tracking-wider">
                    Equipment / Service of Interest
                  </label>
                  <select
                    id="interest"
                    className="w-full bg-[#f8fafc] border border-slate-200 focus:border-[#10b981] px-4 py-3 rounded-md focus:outline-none transition-luxury"
                  >
                    <option>Air Conditioning Systems</option>
                    <option>Cold Rooms & Refrigerator Trailers</option>
                    <option>Specialized Mortuary Equipment</option>
                    <option>Custom Mobile VIP Assets</option>
                    <option>Nationwide Fleet Support Services</option>
                    <option>Custom Relational Blueprints</option>
                  </select>
                </div>

                <div className="flex flex-col gap-2">
                  <label htmlFor="specs" className="font-bold text-slate-500 uppercase tracking-wider">
                    Project Specifications & Dimensions
                  </label>
                  <textarea
                    required
                    id="specs"
                    rows={4}
                    className="w-full bg-[#f8fafc] border border-slate-200 focus:border-[#10b981] px-4 py-3 rounded-md focus:outline-none transition-luxury resize-none"
                    placeholder="Provide details on quantities, physical dimensions, location, and technical requirements..."
                  />
                </div>

                <button
                  type="submit"
                  className="w-full py-4 mt-4 bg-[#01402c] hover:bg-[#02573d] hover:scale-[1.01] active:scale-[0.98] transition-luxury text-white font-bold tracking-wider uppercase rounded-md shadow-[0_4px_14px_rgba(1,64,44,0.15)] cursor-pointer text-center"
                >
                  Submit Specs to Dispatch
                </button>
              </form>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
