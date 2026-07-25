const button=document.querySelector(".theme-toggle");
button?.addEventListener("click",()=>{
  const current=document.documentElement.dataset.theme;
  const next=current==="dark"?"light":"dark";
  document.documentElement.dataset.theme=next;
  localStorage.setItem("theme",next);
});

const tocButton=document.querySelector(".toc-toggle");
const setTocState=(state)=>{
  document.documentElement.dataset.toc=state;
  localStorage.setItem("toc",state);
  tocButton?.setAttribute("aria-expanded",String(state==="open"));
};

if(tocButton){
  setTocState(document.documentElement.dataset.toc);
  tocButton.addEventListener("click",()=>{
    setTocState(document.documentElement.dataset.toc==="open"?"closed":"open");
  });
}

const tocLinks=[...document.querySelectorAll(".article-toc a[href^='#']")];
const headings=tocLinks
  .map(link=>document.getElementById(decodeURIComponent(link.hash.slice(1))))
  .filter(Boolean);

if(headings.length){
  const linksById=new Map(tocLinks.map(link=>[decodeURIComponent(link.hash.slice(1)),link]));
  const observer=new IntersectionObserver(entries=>{
    const visible=entries
      .filter(entry=>entry.isIntersecting)
      .sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top)[0];
    if(!visible)return;
    tocLinks.forEach(link=>link.removeAttribute("aria-current"));
    linksById.get(visible.target.id)?.setAttribute("aria-current","location");
  },{rootMargin:"-15% 0px -70% 0px"});
  headings.forEach(heading=>observer.observe(heading));
}
