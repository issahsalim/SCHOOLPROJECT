const button=document.getElementById('btn')
const indexNumber = [
    'UEB3211422','UEB3211222','UEB3211122'
]

button.addEventListener('click', (e) => {
    const indexnumbers = document.getElementById('indexnumber').value;
    e.preventDefault();
    if (!indexNumber.includes(indexnumbers)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid index number',
            text: 'Please the index number your provide is not in ITB'
        })
    }  
    
})