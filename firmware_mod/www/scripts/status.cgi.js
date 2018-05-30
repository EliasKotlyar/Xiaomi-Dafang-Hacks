$(document).ready(function() {
  $('#formResolution').submit(function(event) {
    var b = $('#resSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'video_size': $('select[name=video_size]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formResolution').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#tzForm').submit(function(event) {
    var b = $('#tzSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tz': $('input[name=tz]').val(),
      'hostname': $('input[name=hostname]').val(),
      'ntp_srv': $('input[name=ntp_srv]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#tzForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#passwordForm').submit(function(event) {
    var b = $('#passwordSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'password': $('input[name=password]').val(),
    };
    $.ajax({
      type: 'POST',
      url: $('#passwordForm').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      showResult(res);
      // reload after 2s
      setTimeout(function() {
        $('#content').load('cgi-bin/status.cgi');
      }, 2000);
    });
    event.preventDefault();
  });

  $('#formOSD').submit(function(event) {
    var b = $('#osdSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    if ($('input[name=OSDenable]').prop('checked')) {
      osdenable = 'enabled';
    } else {
      osdenable = '';
    }
    if ($('input[name=AXISenable]').prop('checked')) {
      axisenable = 'enabled';
    } else {
      axisenable = '';
    }
    var formData = {
      'OSDenable': osdenable,
      'AXISenable': axisenable,
      'osdtext': $('input[name=osdtext]').val(),
      'color': $('select[name=color]').val(),
      'size': $('select[name=size]').val(),
      'spacepixels': $('input[name=spacepixels]').val(),
      'posy': $('input[name=posy]').val(),
      'fixedw': $('select[name=fixedw]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formOSD').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formldr').submit(function(event) {
    var b = $('#ldrSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'avg': $('select[name=avg]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formldr').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });

  $('#formTimelapse').submit(function(event) {
    var b = $('#tlSubmit');
    b.toggleClass('is-loading');
    b.prop('disabled', !b.prop('disabled'));
    var formData = {
      'tlinterval': $('input[name=tlinterval]').val(),
      'tlduration': $('input[name=tlduration]').val()
    };
    $.ajax({
      type: 'POST',
      url: $('#formTimelapse').attr('action'),
      data: formData,
      dataType: 'html',
      encode: true
    }).done(function(res) {
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));
      showResult(res);
    });
    event.preventDefault();
  });
});
