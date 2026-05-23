// JuneGiri — site JS (partials, nav, animations)
(function(){
  'use strict';

  function init(){
    // Mobile nav toggle
    var toggle = document.querySelector('.nav-toggle');
    var links = document.querySelector('.nav-links');
    if(toggle && links){
      toggle.addEventListener('click', function(){
        links.classList.toggle('open');
        toggle.classList.toggle('open');
      });
    }

    // Mobile mega expand: tap parent twice to expand
    if(window.matchMedia('(max-width:900px)').matches){
      document.querySelectorAll('.nav-links > li > a.has-mega').forEach(function(a){
        a.addEventListener('click', function(e){
          if(!a.parentNode.classList.contains('mega-open')){
            e.preventDefault();
            document.querySelectorAll('.nav-links > li.mega-open').forEach(function(li){if(li!==a.parentNode)li.classList.remove('mega-open')});
            a.parentNode.classList.add('mega-open');
          }
        });
      });
    }

    // Highlight active nav
    var path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    var navMap = {
      'index.html':'home','stay.html':'stay','room-jungle.html':'stay','room-river.html':'stay','room-farm.html':'stay','gallery.html':'stay',
      'retreat.html':'retreat','corporate.html':'retreat','ttc.html':'retreat',
      'yatra.html':'yatra','treks.html':'yatra','adventure.html':'yatra',
      'membership.html':'membership',
      'about.html':'about','sustainability.html':'about','press.html':'about','faq.html':'about','contact.html':'about',
      'blog.html':'blog'
    };
    var active = navMap[path];
    if(active){
      document.querySelectorAll('.nav-links a[data-nav]').forEach(function(a){
        if(a.dataset.nav===active) a.classList.add('active');
      });
    }

    // Fade-up
    var fades = document.querySelectorAll('.fade-up');
    if(fades.length && 'IntersectionObserver' in window){
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}
        });
      },{threshold:0.08,rootMargin:'0px 0px -30px 0px'});
      fades.forEach(function(el){io.observe(el);});
    } else {
      fades.forEach(function(el){el.classList.add('visible');});
    }
    setTimeout(function(){
      document.querySelectorAll('.fade-up:not(.visible)').forEach(function(el){el.classList.add('visible');});
    },2500);

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function(a){
      a.addEventListener('click', function(ev){
        var id = a.getAttribute('href');
        var el = document.querySelector(id);
        if(el){ev.preventDefault();var y=el.getBoundingClientRect().top+window.scrollY-70;window.scrollTo({top:y,behavior:'smooth'});}
      });
    });

  }

  // Load partials, then init
  function loadPartial(slot){
    var name = slot.getAttribute('data-include');
    return fetch('partials/'+name+'.html',{cache:'no-cache'}).then(function(r){return r.text();}).then(function(html){
      slot.outerHTML = html;
    }).catch(function(){slot.innerHTML='';});
  }

  var slots = document.querySelectorAll('[data-include]');
  if(slots.length){
    Promise.all(Array.from(slots).map(loadPartial)).then(init);
  } else {
    if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);}else{init();}
  }
})();
