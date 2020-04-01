$(document).ready(function(){
	// Reference to the chat messages area
//  let $chatWindow = $("#messages");
  let $chatWindow = $(".chat-bubbles-body");

  // Our interface to the Chat service
  let chatClient;

  // A handle to the room's chat channel
  let roomChannel;

  let $chat_id;
  let $sender;
  let $receiver;
  let $chat_key;
  $chat_id = document.getElementById("chat_id").value;
  $sender = document.getElementById("sender").value ;
  $receiver = document.getElementById("receiver").value ;

  function pageScroll() {
    window.scrollBy(0,100);
}


  function getchatkey(){
  $.getJSON(
      "/getchatkey",
      {
        chat_id:$chat_id
      },

      function(data)
      {
        $chat_key = data.chat_key;
      }

    ).then(console.log($chat_key));
}
getchatkey();
  console.log($chat_key);
 //let $key = CryptoJS.enc.Utf8.parse($chat_key);

	function print(infoMessage, asHtml) {
    let $msg = $('<div class="info">');
    if (asHtml) {
      $msg.html(infoMessage);
    } else {
      $msg.text(infoMessage);
    }
    $chatWindow.append($msg);
  }
//  function printMessage(fromUser, msg) {
//    console.log($chat_key);
//    var $key = CryptoJS.enc.Utf8.parse($chat_key);
//    var message = decrypt(msg , $key);
//    let $user = $('<span class="username">').text(fromUser + ":");
//    if (fromUser === $sender) {
//      $user.addClass("me");
//    }
//    let $message = $('<span class="message">').text(message);
//    let $container = $('<div class="message-container">');
//    $container.append($user).append($message);
//    $chatWindow.append($container);
//    $chatWindow.scrollTop($chatWindow[0].scrollHeight);
//  }
function printMessage(fromUser,msg){
    console.log($chat_key);
    var $key = CryptoJS.enc.Utf8.parse($chat_key);
    var message = decrypt(msg , $key);
    let $para = "<p>"+(message)+"</p>";
    var container;
    if(fromUser===$sender){
        $container = "<div class='chat-bubble-right'>";

    }else{
        $container = "<div class='chat-bubble-left'>";
    }
    $container+=$para+"</div>"
//    console.log($container.toString());
    $chatWindow.append($container);
    //$(".chat-body-outer").scrollTop($chatWindow[0].scrollHeight);
    pageScroll();


}

  function sendmessage(msg){
  	$.getJSON(
    "/tokenn",  //address
    {
      message: msg
    },
    function(data) {
      printMessage(sender,data.messagefrompython);
    }
  );
  }
  function sendmessagetoserver(msg){
    $.getJSON(
        "/receivemsg",
        {
          chat_id : $chat_id,
          From : $sender,
          To : $receiver,
          message: msg
        },
        function(data){
          if(data.status==="success")
          {
            $received_msg = data.message_from_python;
            console.log($received_msg);
            //$received_msg = decrypt($received_msg,key);
            printMessage($sender , $received_msg);
          }
        }
      )
  }
  function loadpreviousmessages(){
    $.getJSON(
        "/readmsg",
        {
          chat_id:$chat_id
        },
        function(data){
          if(data.status === "success")
          {
            for(i=0;i<data.length;i++)
            {
              printMessage(data.messages[i].from , data.messages[i].message)
            }
          }
        }
      );
  }
  function receivemessgefromserver(){

    $.getJSON(
        "/sendmsg",
       {
          chat_id : $chat_id,
          From : $receiver,
          To : $sender,
        },

    function(data){
      //console.log("Hello");
      if (data.status==="success")
      {
        for(i=0;i<data.length;i++)
        {
          printMessage( $receiver , data.messages[i]);
        }
      }
      setTimeout(receivemessgefromserver , 2000);
    }

    )
  }


function encrypt(msgString, key) {
    // msgString is expected to be Utf8 encoded
    msgString = CryptoJS.enc.Utf8.parse(msgString);
    var iv = CryptoJS.lib.WordArray.random(16);
    var encrypted = CryptoJS.AES.encrypt(msgString, key, {
        iv: iv
    });
    return iv.concat(encrypted.ciphertext).toString(CryptoJS.enc.Base64);
}

function decrypt(ciphertextStr, key) {

    var ciphertext = CryptoJS.enc.Base64.parse(ciphertextStr);

    // split IV and ciphertext
    var iv = ciphertext.clone();
    iv.sigBytes = 16;
    iv.clamp();
    ciphertext.words.splice(0, 4);
    ciphertext.sigBytes -= 16;

    // decryption
    var decrypted = CryptoJS.AES.decrypt({ciphertext: ciphertext}, key, {
        iv: iv
    });
    console.log(decrypted);
    return decrypted.toString(CryptoJS.enc.Utf8);
}


  let $form = $("#message-form");
  let $input = $("#message-input");
  let $send = $("#send");
  $send.on("click", function(e) {
    e.preventDefault();
    let $messagetosend = $input.val().trim();
    if($messagetosend.length!=0){
    var $key = CryptoJS.enc.Utf8.parse($chat_key);
    let $encrypted = encrypt($messagetosend,$key);
    console.log($encrypted);
    sendmessagetoserver($encrypted);
    $input.val('');
    }
  });
  loadpreviousmessages();
  receivemessgefromserver();

});