fetchNotes().then(function(val){
    populateNotes(val);
});

async function fetchNotes(){
    //fetch from firebase the notecollection, and parse document name as its title
    var notecollection;
    var checker = false;
    return $.ajax({
        url: '/',
        data:"test4",
        type: 'POST',
        success: function(response){
            console.log(response);
            notecollection=response;
            checker = true;
        },
        error: function(error){
            console.log(error);
        }
    });
   
}

function populateNotes(notecollection){
    console.log(notecollection)
    const keys = Object.keys(notecollection);

    for(key in keys){  
        console.log(key);
        var notecontent = notecollection[keys[key]];
        addNewNote(notecontent["title"],notecontent["body"],notecontent["color"],notecontent["height"],notecontent["width"],notecontent["left"],notecontent["top"]);
    }
}

function addNewNote(title="title",body=["enter text here"],color="green",height=300,width=100,left=500,top=500){
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
    console.log(left);
    
    notenode.style.backgroundColor = color;
    notenode.style.height=height;
    notenode.style.width=width;
    notenode.style.left=left;
    notenode.style.top=top;

    document.getElementById("noteslist").appendChild(notenode);
    $('.note').draggable();
    $('.note').resizable({'aspectRatio' :true});
}
