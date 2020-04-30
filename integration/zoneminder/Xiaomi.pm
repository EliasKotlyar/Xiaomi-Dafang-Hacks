package ZoneMinder::Control::Xiaomi;

use 5.006;
use strict;
use warnings;
use IO::Socket::SSL;

require ZoneMinder::Base;
require ZoneMinder::Control;

our @ISA = qw(ZoneMinder::Control);

our %CamParams = ();

# ==========================================================================
#
# Xiaomi Dafang Control Protocol
#
# On ControlAddress use the format :
#   USERNAME:PASSWORD@ADDRESS
#   eg : root:ismart@10.0.100.1
#
# ==========================================================================

use ZoneMinder::Logger qw(:all);
use ZoneMinder::Config qw(:all);

use Time::HiRes qw( usleep );

sub new
{

    my $class = shift;
    my $id = shift;
    my $self = ZoneMinder::Control->new( $id );
    my $logindetails = "";
    bless( $self, $class );
    srand( time() );
    return $self;
}

our $AUTOLOAD;

sub AUTOLOAD
{
    my $self = shift;
    my $class = ref( ) || croak( "$self not object" );
    my $name = $AUTOLOAD;
    $name =~ s/.*://;
    if ( exists($self->{$name}) )
    {
        return( $self->{$name} );
    }
        Fatal( "Can't access $name member of object of class $class" );
    }

sub open
{
    my $self = shift;

    $self->loadMonitor();

    use LWP::UserAgent;
    $self->{ua} = LWP::UserAgent->new(
        ssl_opts => {
                verify_hostname => 0,
                SSL_verify_mode => IO::Socket::SSL::SSL_VERIFY_NONE,
         });
    $self->{ua}->agent( "ZoneMinder Control Agent/".ZoneMinder::Base::ZM_VERSION );

    $self->{state} = 'open';
}

sub close
{
    my $self = shift;
    $self->{state} = 'closed';
}

sub printMsg
{
    my $self = shift;
    my $msg = shift;
    my $msg_len = length($msg);

    Debug( $msg."[".$msg_len."]" );
}

sub sendCmd
{
    my $self = shift;
    my $cmd = shift;
    my $result = undef;
    printMsg( $cmd, "Tx" );

    my $req = HTTP::Request->new( GET=>"https://".$self->{Monitor}->{ControlAddress}."/cgi-bin/action.cgi?cmd=$cmd" );
    my $res = $self->{ua}->request($req);

    if ( $res->is_success )
    {
        $result = !undef;
    }
    else
    {
        Error( "Error check failed:'".$res->status_line()."'" );
    }

    return( $result );
}




# Reset the Camera
sub reset
{
    my $self = shift;
    Debug( "Camera Reboot" );
    $self->sendCmd( "reboot" );
}

#Up Arrow
sub moveRelUp
{
    my $self = shift;
    Debug( "Move Up" );
    $self->sendCmd( "motor_up" );
}

#Down Arrow
sub moveRelDown
{
    my $self = shift;
    Debug( "Move Down" );
    $self->sendCmd( "motor_down" );
}

#Left Arrow
sub moveRelLeft
{
    my $self = shift;
    Debug( "Move Left" );
    $self->sendCmd( "motor_left" );
}

#Right Arrow
sub moveRelRight
{
    my $self = shift;
    Debug( "Move Right" );
    $self->sendCmd( "motor_right" );
}

#Home Button
sub presetHome
{
    my $self = shift;
    Debug( "Move Home" );
    $self->sendCmd( "motor_PTZ&x_axis=preset&y_axis=home" );
}

1;
