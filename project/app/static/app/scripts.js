// Simple script to handle navigation and animations

document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll(".framer-links a");

  links.forEach(link => {
    link.addEventListener("click", event => {
      event.preventDefault();
      console.log(`Navigating to ${link.getAttribute("href")}`);
    });
  });
});
