async function delete_item(item_type, id, goto){


    const resp = await fetch(`/delete/${item_type}`, {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "id": id,
        })
    }).then(response=>{
        if (response.status === 200){
            window.location = goto
        }else{
            handle_error(response)
        }
        
    
    })
    
}

async function  handle_error(response){
    data = await response.json()
    error = document.getElementById("error-message")
    error.innerHTML = data["message"]
    error.className = "error"
}