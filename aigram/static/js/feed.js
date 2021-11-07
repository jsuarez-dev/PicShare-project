function likeEvent() {
  const hearts = document.getElementsByClassName('far fa-heart')
  document.ge
  for (const heart of hearts) {
    heart.onclick = (event) => {
      if (event.target.className === "far fa-heart") {
        event.target.className = "fa fa-heart";
      } else {
        event.target.className = "far fa-heart";
      }
    }
  }

}



window.addEventListener('load', () => {
  likeEvent();
})