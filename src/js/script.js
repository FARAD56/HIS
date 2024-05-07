const sidebar = document.querySelector('.sidebar')
const toggle_btn = document.querySelector('.toggle_btn')
const side_text = document.querySelectorAll('#side_text')
const main_body = document.querySelector('.main_body')
const modal = document.getElementById('myModal');
const openButton = document.querySelector('.search');
const closeButton = document.querySelector('.cb');
const overlay = document.getElementById('modalOverlay');
const chat_names = document.querySelector('.chat_names');
const chat_btn = document.querySelector('.chat_btn')

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

closeButton.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
      modal.classList.add('hidden');
    }
  });

chat_btn.addEventListener('click', ()=>{
  chat_names.classList.toggle('chat_names_toggle')
})

