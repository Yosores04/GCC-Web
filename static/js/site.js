(function () {
  function initCarousel(root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll("[data-slide]"));
    if (!slides.length) {
      return;
    }

    var prev = root.querySelector("[data-carousel-prev]");
    var next = root.querySelector("[data-carousel-next]");
    var dotsRoot = root.querySelector("[data-carousel-dots]");
    var intervalMs = Number(root.getAttribute("data-interval") || 5200);
    var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var activeIndex = slides.findIndex(function (slide) {
      return slide.classList.contains("is-active");
    });
    var timer = null;
    var touchStartX = null;

    if (activeIndex < 0) {
      activeIndex = 0;
    }

    function render() {
      slides.forEach(function (slide, index) {
        var isActive = index === activeIndex;
        slide.classList.toggle("is-active", isActive);
        slide.setAttribute("aria-hidden", String(!isActive));
      });

      if (!dotsRoot) {
        return;
      }

      var dots = Array.prototype.slice.call(dotsRoot.querySelectorAll("button"));
      dots.forEach(function (dot, index) {
        var isActive = index === activeIndex;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-selected", String(isActive));
      });
    }

    function goTo(index) {
      var total = slides.length;
      activeIndex = (index + total) % total;
      render();
    }

    function nextSlide() {
      goTo(activeIndex + 1);
    }

    function prevSlide() {
      goTo(activeIndex - 1);
    }

    function stopAuto() {
      if (timer) {
        clearInterval(timer);
        timer = null;
      }
    }

    function startAuto() {
      if (prefersReduced || slides.length < 2) {
        return;
      }
      stopAuto();
      timer = setInterval(nextSlide, intervalMs);
    }

    if (dotsRoot) {
      dotsRoot.innerHTML = "";
      slides.forEach(function (_, index) {
        var dot = document.createElement("button");
        dot.type = "button";
        dot.className = "carousel-dot";
        dot.setAttribute("aria-label", "Go to slide " + (index + 1));
        dot.setAttribute("role", "tab");
        dot.addEventListener("click", function () {
          goTo(index);
          startAuto();
        });
        dotsRoot.appendChild(dot);
      });
    }

    if (next) {
      next.addEventListener("click", function () {
        nextSlide();
        startAuto();
      });
    }
    if (prev) {
      prev.addEventListener("click", function () {
        prevSlide();
        startAuto();
      });
    }

    root.addEventListener("mouseenter", stopAuto);
    root.addEventListener("mouseleave", startAuto);
    root.addEventListener("focusin", stopAuto);
    root.addEventListener("focusout", startAuto);

    root.addEventListener("touchstart", function (event) {
      if (!event.touches || !event.touches.length) {
        return;
      }
      touchStartX = event.touches[0].clientX;
    });

    root.addEventListener("touchend", function (event) {
      if (touchStartX === null || !event.changedTouches || !event.changedTouches.length) {
        touchStartX = null;
        return;
      }

      var deltaX = event.changedTouches[0].clientX - touchStartX;
      touchStartX = null;

      if (Math.abs(deltaX) < 35) {
        return;
      }

      if (deltaX < 0) {
        nextSlide();
      } else {
        prevSlide();
      }
      startAuto();
    });

    render();
    startAuto();
  }

  function boot() {
    var carousels = document.querySelectorAll("[data-carousel]");
    Array.prototype.forEach.call(carousels, initCarousel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
