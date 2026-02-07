
// Typed Text
const containerTyped = document.querySelector('.textTyped');

const skills = ["Graphic Designer", "Freelancer", "Instructor"];
let index = 0;

let characterIndex = 0;

updateText();

function updateText() {
  containerTyped.innerHTML = `
  <h4> I am ${skills[index].slice(0, 1) === "I" ? "an" : "a"} ${skills[index].slice(0, characterIndex)}</h4>
  `;
  characterIndex++;
  if(characterIndex > skills[index].length) {
    characterIndex = 0;
    index++;
    if(index === skills.length) {
      index = 0;
    }
  }

  setTimeout(updateText, 500);
}
// The end of typed text




// ABOUT SECTION CONTENT (TEXTs) DISPLAY FAQs
const contentDisplaysEl = document.querySelectorAll("#content-displays");
const contentRevealsEl = document.querySelectorAll("#content-reveals");


contentDisplaysEl.forEach((icon, index) => {
      
  icon.addEventListener("click", () => {
    contentDisplaysEl.forEach((icon) => {
      icon.classList.remove("rotate-60");
    });

    icon.classList.toggle("rotate-90");
    contentRevealsEl[index].classList.toggle("hidden");
  });
});


//FOR CONTACT FORM IN CONTACT PAGE SECTION
document.querySelector(".contact-form").addEventListener('submit', function(e) {
  const inputs = document.querySelectorAll('input[type="text"], textarea');
  inputs.forEach(input => {
    input.value = input.value.trim();
  });
});