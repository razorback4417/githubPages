document.addEventListener('DOMContentLoaded', function() {
   var a = '';
   if (document.querySelector('#requests')) {
     document.querySelector('#requests').addEventListener('click', () => load_request('requests'));
     a = 'requests';
   };
   if (document.querySelector('#myRequests')) {
     document.querySelector('#myRequests').addEventListener('click', () => load_request('myRequests'));
     a = 'myRequests';
   };
   load_request('')
 });

function load_request(type) {
  console.log(type)
  if (type == 'myRequests') {
    document.querySelector('#requestView').style.display = 'block';
    document.querySelector('#content').style.display = 'none';
    document.querySelector('#requestView').innerHTML = `<h4>My Requests From JS</h4>`;
    console.log("done")
    //var role = "student"
      
    fetch(`/requests`)
      .then(response => response.json())
      .then(data => {
//            console.log(data)
//            console.log(data.length)
//            console.log(typeof data)
            for (i in data) {
                console.log(data[i].fields)
            
                var item = document.createElement("div");
                var subject = JSON.stringify(data[i].fields.subject)
                subject = subject.substring(3, subject.length-3)
            
                var grade = JSON.stringify(data[i].fields.grade)
                grade = grade.substring(3, grade.length-3)
            
            
                var type = null;
                if (data[i].fields.type == 'Become a Tutor') {
                    type = JSON.stringify(data[i].fields.requestor + " is requesting to become a tutor for grade(s) " + grade + " in " + subject)
                }
            
                if (data[i].fields.type == 'Find a Tutor') {
                    var tn = JSON.stringify(data[i].fields.tutorname)
                    tn = tn.substring(1,tn.length-1)
                    type = JSON.stringify(data[i].fields.requestor + " is requesting to be taught in " + subject + " by " + tn)
                }
            
                type = type.substring(1,type.length-1)
            
                var description = JSON.stringify(data[i].fields.description)
                description = description.substring(1, description.length-1)
            
                var status = JSON.stringify(data[i].fields.status)
                status = status.substring(1, status.length-1)
            
                var typeOne = JSON.stringify(data[i].fields.type)
                typeOne = typeOne.substring(1, typeOne.length-1)
            
                var email = JSON.stringify(data[i].fields.req_email)
                email = email.substring(1, email.length-1)
            
                var cd = JSON.stringify(data[i].fields.createdDate)
                cd = cd.substring(1, cd.length-1)
            
                item.innerHTML = `<div class="lead">
                    ${type} <br>
                    <strong> Description: </strong> ${description} <br>
                    <strong> Subject: </strong> ${subject} <br>
                    <strong> Status: </strong> ${status} <br>
                    <strong> Type: </strong> ${typeOne} <br>
                    <strong> Requestor's Email: </strong> ${email} <br>
                    <strong> Created Date: </strong> ${cd}
                    <br><br>
                </div>`;
                document.querySelector("#requestView").appendChild(item)
            }

       })
//    axios.get('/requests')
//      .then(response => {
//        console.log(response.data[0].fields.description);
////        for (int i = 0; i < response.data.length)
//      })
  }
  if (type == 'requests') {
    document.querySelector('#requestViewAdmin').style.display = 'block';
    document.querySelector('#content').style.display = 'none';
    document.querySelector('#requestViewAdmin').innerHTML = `<h4>Requests Testing</h4>`;
      
    fetch(`/requests`)
      .then(response => response.json())
      .then(data => {
            //console.log(data)
            //console.log(typeof data)
            //console.log(data[0].fields.subject)
            
            for (i in data) {
                //console.log(data[i].fields)
            
                var item = document.createElement("div");
                var subject = JSON.stringify(data[i].fields.subject)
                subject = subject.substring(3, subject.length-3)
            
                var grade = JSON.stringify(data[i].fields.grade)
                grade = grade.substring(3, grade.length-3)
            
            
                var type = null;
                if (data[i].fields.type == 'Become a Tutor') {
                    type = JSON.stringify(data[i].fields.requestor + " is requesting to become a tutor for grade(s) " + grade + " in " + subject)
                }
            
                if (data[i].fields.type == 'Find a Tutor') {
                    var tn = JSON.stringify(data[i].fields.tutorname)
                    tn = tn.substring(1,tn.length-2)
                    type = JSON.stringify(data[i].fields.requestor + " is requesting to be taught in " + subject + " by " + tn)
                }
            
                type = type.substring(1,type.length-1)
            
                var description = JSON.stringify(data[i].fields.description)
                description = description.substring(1, description.length-1)
            
                var status = JSON.stringify(data[i].fields.status)
                status = status.substring(1, status.length-1)
            
                var typeOne = JSON.stringify(data[i].fields.type)
                typeOne = typeOne.substring(1, typeOne.length-1)
            
                var email = JSON.stringify(data[i].fields.req_email)
                email = email.substring(1, email.length-1)
            
                var cd = JSON.stringify(data[i].fields.createdDate)
                cd = cd.substring(1, cd.length-1)
            
                item.innerHTML = `<div class="lead">
                    ${type} ${JSON.stringify(data[i].pk)}<br>
                    <strong> Description: </strong> ${description} <br>
                    <strong> Subject: </strong> ${subject} <br>
                    <strong> Status: </strong> ${status} <br>
                    <strong> Type: </strong> ${typeOne} <br>
                    <strong> Requestor's Email: </strong> ${email} <br>
                    <strong> Created Date: </strong> ${cd}
                    <br><br>
                </div>`;
            
                document.querySelector("#requestViewAdmin").appendChild(item);
            
                if (data[i].fields.status == 'Requested') {
            
                    //console.log(i)
                    var j = i
                    //console.log(j)
                    let approveButton = document.createElement("btn");
                    approveButton.innerText = `Approve ${data[i].pk}`
                    //INSERT CLASS NAME FOR SYTLING HERE--> approveButton.className = ``;
                    approveButton.addEventListener("click", () => {
                        processRequest(data[j].pk, 'Approved');
                    });
                    //console.log(approveButton)
                    //console.log("HERE")
                    document.querySelector("#requestViewAdmin").appendChild(approveButton);
                }
            
            }
       })
  }
    
}

function processRequest(id, status) {
    console.log("inside function")
    console.log(id)
    console.log(status)
    fetch(`/requests/${id}/`, {
        method: "PUT",
        body: JSON.stringify({
            decision: status,
        }),
    });
    load_request('requests');
}
