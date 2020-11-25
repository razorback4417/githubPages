function toggle_like(postID) {
    fetch('/toggle_like', {
          method: "POST",
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'X-CSRFToken': document.forms[0].querySelector('input[name="csrfmiddlewaretoken"]').value
          },
          body: JSON.stringify({
            cur_username: cur_username,
            postID: postID,
          })
    })
    
    if (document.querySelector('#likeBtn' + postID).value  ==  "Like") {
        document.querySelector('#likeBtn' + postID).value = "Unlike";
        document.querySelector('#heart' + postID).classList = 'fa fa-heart red';
        document.querySelector('#likeCount' + postID).innerHTML++;
    }
    
    else {
        document.querySelector('#likeBtn' + postID).value = "Like";
        document.querySelector('#heart' + postID).classList = 'fa fa-heart-o';
        document.querySelector('#likeCount' + postID).innerHTML--;
    }
}


function edit_post(postID) {
    oContent = document.querySelector('#entry' + postID).innerHTML;
    
    const elem = document.createElement('div');
    elem.innerHTML = `
        <form>
            <br/>
            <textarea id="newText${postID}" style="width: 80%; border: solid 1px #cccccc;">${oContent}</textarea>
        </form>
    `;
    
    document.querySelector('#editBtn' + postID).innerHTML = "Save";
    let editPostBtn = document.getElementById('editBtn' + postID);
    editPostBtn.setAttribute('onclick', "save_post('" + postID + "')");
    
    document.querySelector('#editTextArea' + postID).append(elem);
}

function save_post(postID) {
    console.log("here in save_post")
    let newContent = document.querySelector('#newText' + postID).value;
    
    document.querySelector('#entry' + postID).innerHTML = newContent;
    document.querySelector('#editTextArea' + postID).style.display = 'none';
    
    fetch('/save_post', {
              method: "POST",
              headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json',
                  'X-CSRFToken': document.forms[0].querySelector('input[name="csrfmiddlewaretoken"]').value
              },
              body: JSON.stringify({
                postID: postID,
                newContent: newContent
              })
        })
    
    console.log("here")
    document.querySelector('#editBtn' + postID).innerHTML = "Edit";
    console.log("here one")
    let editPostBtn = document.getElementById('editBtn' + postID);
    console.log("here two")
    editPostBtn.setAttribute('onclick', "edit_post('" + postID + "')");
    console.log("here three")
}
