fetchNotes().then(function(val){
    populateNotes(val);
});

async function fetchNotes(){
    //fetch from firebase the notecollection, and parse document name as its title
    return $.ajax({
        url: '/',
        data:"test5",
        type: 'POST',
        success: function(response){
            console.log(response);
        },
        error: function(error){
            console.log(error);
        }
    });
   
}

function populateNotes(notecollection){
    const keys = Object.keys(notecollection);

    for(key in keys){  
        var notecontent = notecollection[keys[key]];
        addNewNote(notecontent["title"],notecontent["body"],notecontent["color"],notecontent["height"],notecontent["width"],notecontent["left"],notecontent["top"]);
    }
}

function addNewNote(title="title",body={"enter text here":"emoji"},color="green",height="300px",width="100px",left="500px",top="500px"){
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
    $('.note').resizable({'aspectRatio' :true});
}
