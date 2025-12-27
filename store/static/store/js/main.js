// 1. Get Elements
const hamburger = document.querySelector('.hamburger_menu');
const categoryMenu = document.querySelector('.main_header .category');
const overlay = document.querySelector('#mobile-overlay');
const body = document.body;

// 2. Function to Open Menu

const openMenu = () =>{
    categoryMenu.classList.add('open');
    body.classList.add('menu-open');
}

const closeMenu = () =>{
    categoryMenu.classList.remove('open');
    body.classList.remove('menu-open');
}

// 4. Attach Event Listeners
// Open the menu when the hamburger is clicked
hamburger.addEventListener('click', openMenu);

// Close the menu when the overlay is clicked
overlay.addEventListener('click', closeMenu);