//script below adds functionality to new notes added.
function addNewNote(e,title="title",body={"enter text here":"emoji"},color="green",height="300px",width="100px",left="500px",top="500px"){
    var notenode = document.createElement('div');                
    notenode.classList.add('note');
    notenode.contentEditable='true';
    var header = document.createElement("header");
    header.innerHTML = title;
    header.contentEditable = "true";
    header.classList.add('title')
    notenode.appendChild(header);
    const keys = Object.keys(body);
    for(key in keys){
        var content = keys[key] + ": " +body[keys[key]] ; 
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
    $('.note').droppable({
        drop:function(event,ui){
            console.log(this);
            var listofbody = this.getElementsByClassName('body');
                
            this.insertBefore($( ui.draggable )[0],listofbody[listofbody.length-1].nextSibling);
            listofbody= this.getElementsByClassName('body');
            listofbody[listofbody.length-1].style.left = "0px";
            listofbody[listofbody.length-1].style.top = "0px";

            
        }
    });
    $('.body').draggable();
    $('.note').resizable({'aspectRatio' :true});
}

var newnote = document.getElementById("newnote");
newnote.addEventListener('click',addNewNote);
$('.note').draggable();
$('.note').resizable({'aspectRatio' :true});


