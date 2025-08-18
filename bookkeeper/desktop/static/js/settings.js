

async function change_setting(checkbox, setting){
    value = checkbox.checked

    console.log(setting, value)

    const resp = await fetch("/change-setting", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "setting": setting,
            "value":value
        })
    })

    window.location.reload()

}

async function set_setting(option){


    const resp = await fetch("/change-setting", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify({
            "setting": "mode",
            "value":option.value
        })
    })

    window.location.reload()
}