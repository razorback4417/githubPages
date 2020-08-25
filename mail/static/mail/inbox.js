document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', (event) => submit_email(event));
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  //document.querySelector('#one-email').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  //document.querySelector('#one-email').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `
    <h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>
  `;

  if (mailbox === 'inbox') {
    fetch('/emails/inbox')
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);

        emails.forEach((element) => {
          const elem = document.createElement('div');
          colorBool = "white"
          if (element.read) {
            colorBool = "#d6d6d6"
          }
          elem.innerHTML = `
              <div style="padding-bottom: 0.95px; ">
              </div>
              <div style="class: row; background-color: ${colorBool}; border: solid 1px; border-radius: 5px;">
                <div style="display: inline-block; padding: 5px;">
                  <div style="float: left; width: 250px;">
                    <b> ${element.sender} </b>
                  </div>
                  <div style="float: left; width: 350px;">
                    ${element.subject}
                  </div>
                </div>
                <div style="padding: 5px; display: inline-block; color: grey; float: right;">
                  ${element.timestamp}
                </div>
              </div>
          `;
          elem.addEventListener('click', function() {
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
              let caller = in_email(element.id);
          });
          document.querySelector('#emails-view').append(elem);
        })
        //loop ends above
      });
  }
  if (mailbox === 'sent') {
    fetch('/emails/sent')
      .then(response => response.json())
      .then(emails => {
        // Print emails
        console.log(emails);

        emails.forEach((element) => {
          const elem = document.createElement('div');
          elem.innerHTML = `
              <div style="padding-bottom: 0.95px;">
              </div>
              <div style="class: row; background-color: white; border: solid 1px; border-radius: 5px;">
                <div style="display: inline-block; padding: 5px">
                  <div style="float: left; width: 250px; ">
                    <b> ${element.recipients} </b>
                  </div>
                  <div style="float: left; width: 350px">
                    ${element.subject}
                  </div>
                </div>
                <div style="padding: 5px; display: inline-block; color: grey; float: right;">
                  ${element.timestamp}
                </div>
              </div>
          `;
          elem.addEventListener('click', function() {
              //document.location.href = `http://127.0.0.1:8000/emails/${element.id}`;
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
              let caller = in_email(element.id);
          });
          document.querySelector('#emails-view').append(elem);
        })
        //loop ends above
      });
  }
  if (mailbox === 'archive') {
    fetch('/emails/archive')
      .then(response => response.json())
      .then(emails => {

        // Print emails
        console.log(emails);

        emails.forEach((element) => {
          const elem = document.createElement('div');
          elem.innerHTML = `
              <div style="padding-bottom: 0.95px;">
              </div>
              <div style="class: row; background-color: white; border: solid 1px; border-radius: 5px;">
                <div style="display: inline-block; padding: 5px">
                  <div style="float: left; width: 250px; ">
                    <b> ${element.sender} </b>
                  </div>
                  <div style="float: left; width: 350px">
                    ${element.subject}
                  </div>
                </div>
                <div style="padding: 5px; display: inline-block; color: grey; float: right;">
                  ${element.timestamp}
                </div>
              </div>
          `;
          elem.addEventListener('click', function() {
              //document.location.href = `http://127.0.0.1:8000/emails/${element.id}`;
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
              })
              let caller = in_email(element.id);
          });
          document.querySelector('#emails-view').append(elem);
        })
        //loop ends above
      });
  }

}

function submit_email(event) {
      //prevent from re-submitting form
      event.preventDefault();
      fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        load_mailbox('sent');
    });
}

function in_email(iden) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  //document.querySelector('#one-email').style.display = 'block';
  document.querySelector('#email-view').style.display = 'block';

  document.querySelector('#one-email').innerHTML = '';
  document.querySelector('#reply-view').style.display = 'none';

  fetch(`/emails/${iden}`)
    .then(response => response.json())
    .then(emails => {
      console.log(emails)
      const element = document.createElement('div');
      element.innerHTML = `
        <h4> ${emails.subject} </h4>
        <div style="display: inline-block">
          <b> From: </b> ${emails.sender}
          <div style="display: inline-block; float: right; padding-left: 600px">
            ${emails.timestamp}
          </div>
        </div>
        <div style="color: #b8b8b8">
          <b> to: </b> ${emails.recipients} <br>
        </div>
        <hr>
        <div>
          ${emails.body}
        </div>
      `;

      document.querySelector('#one-email').append(element);

      document.querySelector('#archive').innerHTML = 'Archive';
      archiveOrNot = true
      if (emails.archived === true) {
        archiveOrNot = false;
        document.querySelector('#archive').innerHTML = 'Unarchive';
      }
      document.querySelector('#archive').addEventListener('click', function() {
          fetch(`/emails/${iden}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: archiveOrNot
            })
          })
          load_mailbox('inbox');
      });

      document.querySelector('#reply-email').value = "⏎ Reply"

      //filling in values for Reply
      document.querySelector('#reply-email').addEventListener('click', function() {
        document.querySelector('#reply-view').style.display = 'block';
        document.querySelector('#reply-recipients').value = emails.sender;
        document.querySelector('#reply-subject').value = emails.subject;
        const sub = document.querySelector('#reply-subject').value
        if (sub.includes("Re:")) {
          document.querySelector('#reply-subject').value = emails.subject;
        }
        else {
          document.querySelector('#reply-subject').value = `Re: ${emails.subject}`;
        }
        document.querySelector('#reply-body').value = `\r\n\r\nOn ${emails.timestamp} ${emails.sender} wrote: \r\n${emails.body}\r\n`;

        //reply to email button actions:
        document.querySelector('#reply-form').addEventListener('submit', function() {
          fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: document.querySelector('#reply-recipients').value,
                subject: document.querySelector('#reply-subject').value,
                body: document.querySelector('#reply-body').value
            })
          })
          .then(response => response.json())
          .then(result => {
              console.log(result);
              load_mailbox('sent');
          });
        });
      });

    }) //.then(emails=> ....) ENDS here
}
