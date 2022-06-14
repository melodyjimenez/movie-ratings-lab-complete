
const changeForm = document.querySelector('#change-rating');

changeForm.addEventListener('submit', (evt) => {
    evt.preventDefault();
    const rating = document.querySelector('#change-rating').value;
    alert(rating);
});


//    button.innerHTML = "Rating changed"


// const button = document.querySelector(".change")
// button.addEventListener('click', update_rating)
