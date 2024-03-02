from visualization import explore
import click


@click.command()
@click.argument("variable")
@click.argument("per1")
@click.argument("per2")


def main(variable, per1, per2): 
    explore.given_values_make_plot(variable, per1, per2)

if __name__ == '__main__':
    main()