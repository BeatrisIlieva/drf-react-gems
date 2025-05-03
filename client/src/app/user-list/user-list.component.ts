import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
} from '@angular/core';
import { User } from '../types/user';

@Component({
    selector: 'app-user-list',
    templateUrl: './user-list.component.html',
    styleUrls: ['./user-list.component.css'],
    // changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserListComponent {
    isToggle = false;

    @Input('users') userListData: User[] = [];

    handleClick(event: Event) {
        console.log('clicked!', event);

        this.isToggle = !this.isToggle;
    }

    // constructor(private cd: ChangeDetectorRef) {
    //     setInterval(() => {
    //         this.cd.detectChanges();
    //         console.log('Changes detected');
    //     }, 3000);
    // }
}
