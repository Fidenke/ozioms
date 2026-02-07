//aboutBtn

// CAROUSEL BOOTSTRAP
const myCarouselElement = document.querySelector('#myCarousel')

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 2000,
  touch: false
})
// End Of CAROUSEL BOOTSTRAP

//Bootstap modal
const myModal = document.getElementById('myModal')
const myInput = document.getElementById('myInput')

myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})
// End Of Bootstap modal

//About Button
const aboutBtn = document.querySelector('#aboutBtn')

aboutBtn.addEventListener('click', () => {
  myModal.show()
})
// End Of About Button  
//Scroll To Top Button
const scrollToTopBtn = document.querySelector('#scrollToTopBtn')

window.addEventListener('scroll', () => {
  if (window.pageYOffset > 300) {
    scrollToTopBtn.style.display = 'block'
  } else {
    scrollToTopBtn.style.display = 'none'
  }
})

scrollToTopBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior:'smooth'
  })
})
// End Of Scroll To Top Button
