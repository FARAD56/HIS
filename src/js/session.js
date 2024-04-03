const toggleButton = document.querySelector('#dropdownToggle');
const dropdownPanel = document.querySelector('.dropdownPanel'); 
const sidebar = document.querySelector('.sidebar')
const toggle_btn = document.querySelector('.toggle_btn')
const side_text = document.querySelectorAll('#side_text')
const main_body = document.querySelector('.main_body')
const modal = document.getElementById('myModal');
const openButton = document.querySelector('.search');
const closeButton = document.querySelector('.cb'); // Updated selector
const overlay = document.getElementById('modalOverlay'); // Updated overlay selector

toggle_btn.addEventListener('click', ()=>{
    sidebar.classList.toggle('toggle_sidebar')
    side_text.forEach((element)=>{
        element.classList.toggle('toggle_text')
    })
    main_body.classList.toggle('toggle_main_body') 
    
})

openButton.addEventListener('click', () => {
    modal.classList.remove('hidden');
  });

  // Close modal when clicking the close button
  closeButton.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

  // Close modal when clicking the overlay
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      modal.classList.add('hidden');
    }
  });

 // Toggle dropdown visibility on button click
  toggleButton.addEventListener('click', () => {
    dropdownPanel.classList.toggle('dropdown_active');
  });
  
  // Close dropdown when clicking anywhere outside
  document.addEventListener('click', (event) => {
    if (!toggleButton.contains(event.target) && !dropdownPanel.contains(event.target)) {
      dropdownPanel.classList.remove('dropdown_active');
    }
  });