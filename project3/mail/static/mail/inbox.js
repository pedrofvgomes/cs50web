document.addEventListener('DOMContentLoaded', function () {

  let emailview = document.createElement('div');
  emailview.id = 'email-view';
  document.querySelector('.container').appendChild(emailview);
  document.querySelector('#email-view').style.display = 'none'

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');


  // compose mail
  document.querySelector('#compose-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the form from actually submitting

    // POST request to send the email
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

        // After sending the email, load the 'sent' mailbox
        load_mailbox('sent');
      });
  });
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#emails-view').style.fontSize = 'medium';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Create a container for holding email content
  let emailContainer = document.createElement('div');

  // Load emails
  let url = '/emails/' + String(mailbox);

  fetch(url)
    .then(response => response.json())
    .then(emails => {
      emails.forEach(email => {
        let emailDiv = document.createElement('div');
        emailDiv.classList.add('email');
        emailDiv.id = email.id;
        emailDiv.innerHTML = `
          <span class="email-sender">${email.sender}</span>
          <span class="email-subject">${email.subject}</span>
          <span class="email-timestamp">${email.timestamp}</span>
        `;
        if (email.read) emailDiv.style.backgroundColor = 'lightgrey';
        else emailDiv.style.backgroundColor = 'white';
        emailDiv.style.textDecoration = 'none';
        emailDiv.style.color = 'black';
        emailDiv.style.border = 'solid 1px black';
        emailDiv.style.borderRadius = '15px';
        emailDiv.style.padding = '1em';
        emailDiv.style.display = 'flex';
        emailDiv.style.fontSize = 'larger';
        emailDiv.style.marginBottom = '0.5em';

        emailDiv.querySelector('.email-sender').style.fontWeight = 'bold';
        emailDiv.querySelector('.email-subject').style.marginLeft = '2em';
        emailDiv.querySelector('.email-subject').style.marginRight = 'auto';
        emailDiv.querySelector('.email-timestamp').style.fontWeight = 'lighter';
        emailDiv.querySelector('.email-timestamp').style.marginRight = '1em';

        emailContainer.appendChild(emailDiv);
        emailDiv.addEventListener('mouseover', function () {
          emailDiv.style.cursor = 'pointer';
        });
        emailDiv.addEventListener('click', function () {
          document.querySelector('#emails-view').style.display = 'none';
          document.querySelector('#email-view').style.display = 'block';
          document.querySelector('#compose-view').style.display = 'none';

          // recolher dados
          fetch('/emails/' + emailDiv.id)
            .then(response => response.json())
            .then(data => {
              let emailViewHTML = `
            <p><strong>From: </strong>${data.sender}</p>
            <p><strong>To: </strong>${data.recipients.join(', ')}</p>
            <p><strong>Subject: </strong>${data.subject}</p>
            <p><strong>Timestamp: </strong>${data.timestamp}</p>
            <button class='btn btn-sm btn-outline-primary' id="reply">Reply</button>
          `; if (mailbox != 'sent') {
                if (!data.archived) emailViewHTML += `<button class='btn btn-sm btn-outline-primary' id="archive">Archive</button>`;
                else emailViewHTML += `<button class='btn btn-sm btn-outline-primary' id="archive">Unarchive</button>`;
              }

              document.querySelector('#email-view').innerHTML = emailViewHTML;
              document.querySelector('#email-view').style.fontSize = 'large';

              // botao de arquivar
              if (mailbox != 'sent')
                document.querySelector('#archive').addEventListener('click', function () {
                  fetch('/emails/' + emailDiv.id, {
                    method: 'PUT',
                    body: JSON.stringify({
                      archived: !data.archived
                    })
                  })
                    .then(load_mailbox('inbox')).then(location.reload());
                })

              // botao de responder
              document.querySelector('#reply').addEventListener('click', function(){
                compose_email();
                
                // pre-fill recipients
                document.querySelector('#compose-recipients').value = data.sender;

                // pre-fill subject
                if(data.subject.slice(0,3) != 'Re:') document.querySelector('#compose-subject').value = 'Re: ' + data.subject;
                else data.querySelector('#compose-subject').value = data.subject;
                
                // pre-fill body
                document.querySelector('#compose-body').value = `On ${data.timestamp}, ${data.sender} wrote:\n${data.body}`; 
              })
            });

          // marcar como lido
          fetch('/emails/' + emailDiv.id, {
            method: 'PUT',
            body: JSON.stringify({
              read: true
            })
          })
        });
      });

      // Append the email container to the emails-view element
      document.querySelector('#emails-view').appendChild(emailContainer);
    });
}