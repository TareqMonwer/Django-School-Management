(function($) {
  "use strict";

  var currentPath = window.location.pathname;

  // ── Sidebar dropdown toggle ──
  $(".sidebar .sidebar-menu > li.dropdown > a").on("click", function(e) {
    var $li = $(this).parent();
    var $sub = $li.children(".dropdown-menu");
    if (!$sub.length) return;

    e.preventDefault();

    if ($li.hasClass("open")) {
      $sub.slideUp(200, function() {
        $li.removeClass("open");
      });
    } else {
      $li.siblings("li.open").each(function() {
        var $sib = $(this);
        $sib.children(".dropdown-menu").slideUp(200);
        $sib.removeClass("open");
      });
      $li.addClass("open");
      $sub.slideDown(200);
    }
  });

  // ── Active link detection ──
  var $menu = $(".sidebar .sidebar-menu");
  var $active = null;
  var bestLen = 0;

  $menu.find("a.sidebar-link").each(function() {
    var href = $(this).attr("href");
    if (!href || href.length < 2 || href === "#") return;

    var normHref = href.replace(/\/+$/, "");
    var normPath = currentPath.replace(/\/+$/, "");

    if (normPath === normHref) {
      $active = $(this);
      bestLen = href.length;
      return false;
    }
    if (currentPath.indexOf(href) === 0 && href.length > bestLen) {
      bestLen = href.length;
      $active = $(this);
    }
  });

  if ($active && $active.length) {
    $menu.find("a.sidebar-link").removeClass("active");
    $active.addClass("active");
    $active.closest("li").addClass("actived");

    var $parentDropdown = $active.closest("li.dropdown");
    if ($parentDropdown.length) {
      $parentDropdown.addClass("open");
      $parentDropdown.children(".dropdown-menu").css("display", "block");
    }
  }

  // ── Sidebar collapse toggle ──
  $("[data-toggle-sidebar], .sidebar-toggle").on("click", function(e) {
    e.preventDefault();
    $("body.app").toggleClass("is-collapsed");
  });

  // ── Header search toggle ──
  $(".search-toggle, .search-box .search-icon").closest("a").on("click", function(e) {
    e.preventDefault();
    var $box = $(this).closest(".search-box");
    $box.toggleClass("active");
    $box.closest("ul").find(".search-input").toggleClass("active");
  });

  // ── Masonry init (if library loaded) ──
  if (typeof Masonry !== "undefined" && $(".masonry").length) {
    window.addEventListener("load", function() {
      new Masonry(".masonry", {
        itemSelector: ".masonry-item",
        columnWidth: ".masonry-sizer",
        percentPosition: true
      });
    });
  }

})(jQuery);
