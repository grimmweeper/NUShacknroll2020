populateNotes(fetchNotes());

function fetchNotes(){
    //fetch from firebase the notecollection, and parse document name as its title
    $.get("{{url_for('echo')}}",function(data,status){
        console.log(data);
        console.log(status);
    });
    var notecollection = [{"title": "To-Do","body":["item1","item2","item3"],"color":"red","height":"300px","width":"100px","left":"200px","top":"100px"},
    {"title": "To-Do","body":["item1","item2","item3"],"color":"green","height":"300px","width":"100px","left":"400px","top":"200px"},
    {"title": "To-Do","body":["item1","item2","item3"],"color":"blue","height":"300px","width":"100px","left":"600px","top":"300px"}]

    return notecollection;
}

function populateNotes(notecollection){
    for(note in notecollection){  
        var notecontent = notecollection[note];
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
