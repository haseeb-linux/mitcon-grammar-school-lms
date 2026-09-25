/* Mitcon Grammar School LMS - Main JavaScript */

document.addEventListener("DOMContentLoaded", () => {
  console.log("Mitcon LMS loaded ✅");

  // Auto-dismiss alerts after 5 seconds
  document.querySelectorAll(".alert").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity 0.5s";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 500);
    }, 5000);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  // Navbar shadow on scroll
  const navbar = document.querySelector(".school-navbar");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 20) {
        navbar.style.boxShadow = "0 4px 20px rgba(0,0,0,0.1)";
      } else {
        navbar.style.boxShadow = "0 2px 10px rgba(26,35,126,0.1)";
      }
    });
  }
});