// ...existing code...
import React from "react";

export const CloudAnimation: React.FC = () => {
  return (
    <div className="clouds-fixed" aria-hidden="true">
      <style>{`
        .clouds-fixed {
          position: fixed;
          inset: 0;
          width: 100%;
          height: 100%;
          overflow: hidden;
          pointer-events: none;
          z-index: 0;
        }

        .cloud {
          position: absolute;
          will-change: transform, opacity;
          opacity: 0.95;
        }

        @keyframes floatX {
          0% { transform: translateX(-40vw); }
          100% { transform: translateX(140vw); }
        }

        /* Staggered clouds across the page; negative delays make them appear mid-flight on mount */
        .c1 { top: 6%; left: -30%; animation: floatX 50s linear infinite; animation-delay: -15s; }
        .c2 { top: 22%; left: -30%; animation: floatX 68s linear infinite; animation-delay: -34s; opacity:0.95; }
        .c3 { top: 44%; left: -30%; animation: floatX 62s linear infinite; animation-delay: -48s; opacity:0.9; }
        .c4 { top: 66%; left: -30%; animation: floatX 76s linear infinite; animation-delay: -60s; opacity:0.92; }

        /* sizes */
        .c1 svg { width: 420px; height: auto; }
        .c2 svg { width: 240px; height: auto; }
        .c3 svg { width: 360px; height: auto; }
        .c4 svg { width: 280px; height: auto; }

        /* subtle parallax: slower clouds slightly more transparent */
        .c2 { opacity: 0.9; }
        .c3 { opacity: 0.85; }
      `}</style>

      {/* Cloud 1 */}
      <div className="cloud c1">
        <svg
          viewBox="0 0 64 40"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          focusable="false"
        >
          <g fill="#ffffff" stroke="none">
            <path d="M20 10a8 8 0 0 0-8 8 6 6 0 0 0 0 .5H8a6 6 0 0 0 0 12h36a8 8 0 0 0 0-16 10 10 0 0 0-18-4z" />
          </g>
        </svg>
      </div>

      {/* Cloud 2 */}
      <div className="cloud c2">
        <svg
          viewBox="0 0 64 40"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          focusable="false"
        >
          <g fill="#ffffff" stroke="none">
            <path d="M18 12a7 7 0 0 0-7 7 5 5 0 0 0 0 .4H7a5 5 0 0 0 0 10h34a7 7 0 0 0 0-14 9 9 0 0 0-25-3z" />
          </g>
        </svg>
      </div>

      {/* Cloud 3 */}
      <div className="cloud c3">
        <svg
          viewBox="0 0 80 48"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          focusable="false"
        >
          <g fill="#ffffff" stroke="none">
            <path d="M24 14a9 9 0 0 0-9 9 7 7 0 0 0 0 .5H10a7 7 0 0 0 0 14h44a9 9 0 0 0 0-18 12 12 0 0 0-30-5z" />
          </g>
        </svg>
      </div>

      {/* Cloud 4 */}
      <div className="cloud c4">
        <svg
          viewBox="0 0 64 40"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
          focusable="false"
        >
          <g fill="#ffffff" stroke="none">
            <path d="M22 11a8 8 0 0 0-8 8 6 6 0 0 0 0 .5H10a6 6 0 0 0 0 12h36a8 8 0 0 0 0-16 10 10 0 0 0-18-4z" />
          </g>
        </svg>
      </div>
    </div>
  );
};

export default CloudAnimation;
// ...existing code...
