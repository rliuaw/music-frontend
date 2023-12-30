function setupSongsDisplay(pl, playlist) {
    // Setup the playlist display. Also used for search

    var ul = null;
    // var ulth = 1;
    playlist.forEach(function (song) {
    var li = document.createElement('li');
    li.className = 'pure-menu-item';
    if (song.file == null) {
        // Title
        if (ul != null) {
        pl.appendChild(ul);
        }
        li.innerHTML = song.title;
        // jpGameTitles.push(song.title);
        li.id = song.code;
        li.className += ' pure-menu-disabled playlist-title';
        ul = document.createElement('ul');
        ul.className = 'pure-menu-list';
        // if (ulth > 5) {
        //   ul.style.backgroundImage = 'url(\'./images/title/' + ('00' + ulth).slice(-2) + '.jpg\')';
        // }
        // ulth++;
    } else {
        // Song
        var a = document.createElement('div');
        a.innerHTML = song.title;
        // jpSongTitles.push(song.title);
        a.className = 'pure-menu-link playlist-item';
        a.id = `${song.file}`
        a.setAttribute('song-index', playlist.indexOf(song));
        a.onclick = function () {
        player.skipTo(playlist.indexOf(song));
        };
        li.appendChild(a);
    }
    ul.appendChild(li);
    });
    pl.appendChild(ul);
}

function filterSearchResults(input, results) {
    filter = input.value.toUpperCase();
    li = results.getElementsByTagName('li');
    for (i = 0; i < li.length; i++) {
        item = li[i].getElementsByClassName('playlist-item')[0] || li[i];
        txtValue = item.textContent || item.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "list-item";
        } else {
            li[i].style.display = "none";
        }
    }
}