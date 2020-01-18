//script below adds functionality to new notes added.
function addNewNote(e,title="title",body=["enter text here"],color="green",height=300,width=100,left=500,top=500){
    var notenode = document.createElement('div');                
    notenode.classList.add('note');
    notenode.contentEditable='true';
    var header = document.createElement("header");
    header.innerHTML = title;
    header.contentEditable = "true";
    header.classList.add('title')
    notenode.appendChild(header);
    for(index in body){
        var content = body[index]; 
        var body1 = document.createElement("body");
        body1.innerHTML = content;
        body1.contentEditable="true";
        body1.classList.add('body');
        notenode.appendChild(body1);
    }

    notenode.style.backgroundColor = color;
    notenode.style.height=height;
    notenode.style.width=width;
    notenode.style.left=left;
    notenode.style.top=top;

    document.getElementById("noteslist").appendChild(notenode);
    $('.note').draggable();
    $('.note').resizable({'aspectRatio' :true});
}

var newnote = document.getElementById("newnote");
newnote.addEventListener('click',addNewNote);
$('.note').draggable();
$('.note').resizable({'aspectRatio' :true});


