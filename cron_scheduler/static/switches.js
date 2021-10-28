setInterval(function(){
    document.querySelectorAll('.switch').forEach(element=>{ 
        fetch("getState/"+element.id)
        .then(res=>res.text())
        .then(data=>document.getElementById(element.id).checked = (data=='True'))
    })
},5000)

function setState(id){
    fetch('setState/'+id+'/'+(+document.getElementById(id).checked))
}
