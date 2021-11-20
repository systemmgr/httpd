<!DOCTYPE html>
<html>

<head>
  <title>Domain Doesn't Exist</title>
  <link rel="stylesheet" href="https://bootswatch.com/4/darkly/bootstrap.css">
  <link rel="stylesheet" href="/default-css/casjaysdev.css">
  <link rel="stylesheet" href="/default-css/errorpages/default.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css">
  <script src="/default-js/errorpages/isup.js"></script>
  <script src="/default-js/errorpages/homepage.js"></script>
  <script src="/default-js/errorpages/loaddomain.js"></script>
  <?php include "https://static.casjay.net/casjays-header.php"; ?>
  <link rel="icon" href="/default-icons/favicon.png"  type="image/icon png">
</head>

<body>
  <br><br>
  <div class="c1">
    <h2>UMMMMM<br>
      This site doesn't seem to exist<br>
    </h2><br><br>
    <img alt='error' src='/default-icons/errors/404.gif'>
    <br><br><br>
  </div>
  <div class="c5">
    <br>
    <?php  echo "Server Name: " . $_SERVER['SERVER_NAME'] . "<BR>"; ?>
    <?php echo "IP Address: " . $_SERVER['SERVER_ADDR'] . "<BR>"; ?>
    <br><br>
    Linux OsVer: <?php echo shell_exec('cat /etc/redhat-release | grep 'BUILD_ID' | awk -F '=' '{print $2}''); ?><br>
    ConfigVer: <?php echo shell_exec( 'cat /etc/casjaysdev/updates/versions/configs.txt' ); ?>
    <br><br>
    Powered by a Redhat based system<br>
    <a href="https://redhat.com"> <img border="0" alt="Redhat/CentOS/Fedora/SL Linux" src="/default-icons/powered_by_redhat.jpg"> </a><br>
    <br><br><br><br><br>
  </div>
  <!-- Begin Casjays Developments Footer -->
  <center>
    <?php include "https://static.casjay.net/casjays-footer.php"; ?>
  </center>
  <!-- End Casjays Developments Footer -->
</body>

</html>
