const button=document.querySelector(".theme-toggle");
button?.addEventListener("click",()=>{
  const current=document.documentElement.dataset.theme;
  const next=current==="dark"?"light":"dark";
  document.documentElement.dataset.theme=next;
  localStorage.setItem("theme",next);
});

const statusLine=document.querySelector("#current-status[data-status-url]");
if(statusLine){
  fetch(statusLine.dataset.statusUrl)
    .then(response=>{
      if(!response.ok)throw new Error("Status list unavailable");
      return response.json();
    })
    .then(statuses=>{
      if(!Array.isArray(statuses)||!statuses.length)return;
      const previous=sessionStorage.getItem("shiori-status");
      const choices=statuses.filter(status=>status!==previous);
      const pool=choices.length?choices:statuses;
      const status=pool[Math.floor(Math.random()*pool.length)];
      statusLine.textContent=status;
      sessionStorage.setItem("shiori-status",status);
    })
    .catch(()=>{});
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
    document.querySelectorAll(".article-toc li.is-active-branch")
      .forEach(item=>item.classList.remove("is-active-branch"));
    const currentLink=linksById.get(visible.target.id);
    currentLink?.setAttribute("aria-current","location");
    let branch=currentLink?.closest("li");
    while(branch){
      branch.classList.add("is-active-branch");
      branch=branch.parentElement?.closest("li");
    }
  },{rootMargin:"-15% 0px -70% 0px"});
  headings.forEach(heading=>observer.observe(heading));
}
