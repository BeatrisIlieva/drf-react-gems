import {
    Component,
    EventEmitter,
    Input,
    OnDestroy,
    OnInit,
    Output,
} from '@angular/core';

type User = {
    name: string;
    age: number;
    status?: string;
};

@Component({
    selector: 'app-playground',
    templateUrl: './playground.component.html',
    styleUrls: ['./playground.component.css'],
})
export class PlaygroundComponent implements OnInit, OnDestroy {
    @Input('color') colorValue = 'white';
    @Output() onTestOutput = new EventEmitter<string>();

    isToggle = false;
    badCurly = 'bad-curly';
    imageUrl =
        'https://images.unsplash.com/photo-1746202382547-ecc40a122aed?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHw0fHx8ZW58MHx8fHx8';

    ngOnInit() {
        console.log('Component created');
    }

    ngAfterViewInit() {
        console.log('After init');
    }

    ngOnDestroy() {
        console.log('on desstrouy');
    }

    ngDoCheck() {
        console.log({ isToggle: this.isToggle });
    }

    users = [
        { name: 'Pesho', age: 20, status: 'green' },
        { name: 'Pesho', age: 20, status: 'yellow' },
        { name: 'Pesho', age: 20 },
        { name: 'Pesho', age: 20, status: 'orange' },
        { name: 'Pesho', age: 20 },
    ] as User[];

    handleClick(event: Event) {
        console.log('clicked!', event);

        this.isToggle = !this.isToggle;
    }

    handleInput(usernameValue: string) {
        console.log(usernameValue);

        console.log(this.colorValue);

        this.onTestOutput.emit(usernameValue || '');
    }
}
