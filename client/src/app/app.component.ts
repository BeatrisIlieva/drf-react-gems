import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
} from '@angular/core';
import { User } from './types/user';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent {
    title = 'client';

    users: User[] = [
        { name: 'Pesho', age: 20 },
        { name: 'Pesho', age: 20 },
        { name: 'Pesho', age: 20 },
        { name: 'Pesho', age: 20 },
        { name: 'Pesho', age: 20 },
    ];

    addUser(inputName: HTMLInputElement, inputAge: HTMLInputElement) {
        const user: User = {
            name: inputName.value,
            age: Number(inputAge.value),
        };

        this.users = [...this.users, user]
        // this.users.push(user);

        inputName.value = '';
        inputAge.value = '';
    }

    colorRedForPlayground = 'red';
    colorGreenForPlayground = 'green';

    onOutputFromChild(inputValue: string) {
        console.log('from parent', inputValue);
    }

    // constructor(private cd: ChangeDetectorRef) {
    //     // setTimeout(() => {
    //     //     this.title = 'Changed from Angular';
    //     // }, 3000);

    //     setInterval(() => {
    //         this.cd.detectChanges();
    //         console.log('Changes detected');
            
    //     }, 3000);
    // }

    // constructor(private cd: ChangeDetectorRef) {
    //     setTimeout(() => {
    //         this.title = 'Changed from detector';
    //         this.cd.detectChanges();
    //     }, 3000)
    // }
}
