const button=document.querySelector(".theme-toggle");
button?.addEventListener("click",()=>{
  const current=document.documentElement.dataset.theme;
  const next=current==="dark"?"light":"dark";
  document.documentElement.dataset.theme=next;
  localStorage.setItem("theme",next);
});

